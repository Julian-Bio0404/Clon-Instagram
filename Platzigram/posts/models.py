"""Posts models."""

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from users.models import Profile


class Post(models.Model):
    """Post model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="posts/photos")
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username"""
        return "{} by @{}".format(self.title, self.user.username)
    
    class Meta:
        """Meta class."""
        ordering = ["-created"]


class Like(models.Model):
    """Like model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return title and username"""
        return "{} has liked {}".format(self.user.username, self.post)


class Comment(models.Model):
    """Comment model."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return username, post title and comment."""
        return "@{} has commented {} on {}".format(self.user.username, self.comment, self.post)
