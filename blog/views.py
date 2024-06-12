from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostReaction
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

def post_detail(request, pk):
    posts = Post.objects.filter(id=pk)
    return render(request, 'blog/post_detail.html', {'posts': posts})

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
        'rating': post.rating
    } for post in posts_page.object_list]

    return JsonResponse({
        'posts': post_list,
        'has_next': posts_page.has_next()
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
    posts_to_count = Post.objects.filter(author=profile_user)
    posts = posts_to_count[:2]
    print(request.user)
    print(profile_user.username)
    post_count = posts_to_count.count()  # Count the number of posts
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