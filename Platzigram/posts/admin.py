"""Admin Posts"""

# Django
from django.contrib import admin

# Models
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Posts Admin model"""

    list_display = ('pk', 'user', "title", 'photo')
    search_fields = ('title', 'user__username', "user__email")
    list_filter = ('created', 'modified')
