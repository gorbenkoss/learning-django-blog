from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm


# Create your tests here.
class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='hNBQd$2MJ#4.!F6')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            is_public=True,
            rating=0
        )

    def test_post_content(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.is_public, True)
        self.assertEqual(self.post.rating, 0)

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            is_public=True,
            rating=0
        )

    def test_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        print(response.content.decode())  # Debugging: Print the response content
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_create_post_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post-new'), {
            'title': 'Another Test Post',
            'content': 'This is another test post.',
            'is_public': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after post creation
        self.assertEqual(Post.objects.count(), 2)  # Two posts now exist

    def test_like_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('like-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.rating, 1)

    def test_dislike_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('dislike-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.rating, -1)


class PostFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=user,
            is_public=True,
            rating=0
        )
        data = {'title': 'Test Post', 'content': 'This is a test post.', 'is_public': True}
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'title': '', 'content': 'This is a test post.'}  # Title is required
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())

