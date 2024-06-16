from django.contrib import admin
from .models import Post, PostReaction, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'is_public', 'rating')
    list_filter = ('is_public', 'date_posted')
    search_fields = ('title', 'content')


class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'liked', 'date_created')
    list_filter = ('liked', 'date_created')
    search_fields = ('user__username', 'post__title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'date_posted', 'author', 'parent_post')
    list_filter = ('date_posted', 'author')
    search_fields = ('content', 'author__username', 'parent_post__title')

admin.site.register(PostReaction, PostReactionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# Register your models here.
