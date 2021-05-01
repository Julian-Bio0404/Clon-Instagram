"""Users models."""

# Django
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Profile model.
    Model 1:1 with User"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to="users/pictures", 
        blank=True, 
        null=True
        )
        
    count_post = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username


class Follow(models.Model):
    """Follow model.
    total following and followers"""

    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


