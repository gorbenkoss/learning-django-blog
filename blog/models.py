from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    is_public = models.BooleanField(default=True) 
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author} on {self.parent_post}'


class PostReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    liked = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=10) 

    class Meta:
        unique_together = ('user', 'post', 'comment')  # Ensure each user can only react once per post

