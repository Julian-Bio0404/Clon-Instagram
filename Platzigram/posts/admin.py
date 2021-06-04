"""Admin Posts"""

# Django
from django.contrib import admin

# Models
from posts.models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Posts Admin model"""

    list_display = ('pk', 'user', "title", 'photo', "likes")
    search_fields = ('title', 'user__username', "user__email")
    list_filter = ('created', 'modified')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin model."""

    list_display = ('pk', 'user', "post", "comment")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Like Admin model."""

    list_display = ("pk", "user", "post")
