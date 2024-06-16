from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CustomUserCreationForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostReaction, Comment
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.timezone import localtime

def home(request):
    return render(request, 'blog/home.html')

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # assuming the user is logged in
            post.save()
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            return redirect('post-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

def post_detail(request, pk):
    posts = Post.objects.filter(pk=pk)
    post = posts.first()
    comments_list = Comment.objects.filter(parent_post=post).order_by('-date_posted')
    comment_form = CommentForm()
    paginator = Paginator(comments_list, 2)  # Show 5 comments per page
    comments = paginator.get_page(1)  # Get the first page of comments
    comment_form = CommentForm()
    total_comments = comments_list.count()

    context = {
        'posts': posts,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'total_comments': total_comments,
    }
    return render(request, 'blog/post_detail.html', context)  

def load_more_posts(request):
    page_number = request.GET.get('page')
    username = request.GET.get('username')

    if username:
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user, is_public=True).order_by('-date_posted')
    else:
        posts = Post.objects.filter(is_public=True).order_by('-date_posted')

    paginator = Paginator(posts, 2)
    posts_page = paginator.get_page(page_number)

    post_list = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': localtime(post.date_posted).isoformat(),
        'author': post.author.username,
        'can_edit': post.author == request.user,
        'rating': post.rating,
        'comments_count': post.comments.count()  # Add this line

    } for post in posts_page.object_list]

    return JsonResponse({
        'posts': post_list,
        'has_next': posts_page.has_next()
    })

def load_more_comments(request, pk):
    comments_list = Comment.objects.filter(parent_post=pk).order_by('-date_posted')
    paginator = Paginator(comments_list, 2)  # Load 2 comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = []

    comments_list = [{
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'date_posted': localtime(comment.date_posted).isoformat()
    } for comment in comments.object_list]

    return JsonResponse({
        'comments': comments_list,
        'has_next': comments.has_next() if hasattr(comments, 'has_next') else False
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog-home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def account(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user)
    print(request.user)
    print(profile_user.username)
    post_count = posts.count()  # Count the number of posts
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'post_count': post_count
    }
    return render(request, 'blog/account.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    reaction, created = PostReaction.objects.get_or_create(user=request.user, post=post)
    if not created and reaction.liked:
        return JsonResponse({'rating': post.rating})  # No change if already liked
    if not created and not reaction.liked:
        post.rating += 1  # Switching from dislike to like
    elif created:
        post.rating += 1  # First time like
    reaction.liked = True
    reaction.save()
    post.save()
    return JsonResponse({'rating': post.rating})

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    reaction, created = PostReaction.objects.get_or_create(user=request.user, post=post)
    if not created and not reaction.liked:
        return JsonResponse({'rating': post.rating})  # No change if already disliked
    if not created and reaction.liked:
        post.rating -= 1  # Switching from like to dislike
    elif created:
        post.rating -= 1  # First time dislike
    reaction.liked = False
    reaction.save()
    post.save()
    return JsonResponse({'rating': post.rating})