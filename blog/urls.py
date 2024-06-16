from django.urls import path
from . import views
from .views import account, load_more_posts, load_more_comments
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/new/', views.post_new, name='post-new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add-comment'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog-home'), name='logout'),
    path('account/<str:username>/', account, name='account'),
    path('ajax/load_more_posts/', load_more_posts, name='load-more-posts'),
    path('post/<int:pk>/load-more-comments/', load_more_comments, name='load-more-comments'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike-post'),
]