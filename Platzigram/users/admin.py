"""User admin"""

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

# Models
from users.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin.

        profile data list"""

    list_display = ("pk", "user", "phone_number", "website", "picture")
    list_display_links = ("pk", "user")
    list_editable = ("phone_number", "website", "picture")
    
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name", 
        "user__last_name", 
        "phone_number"
        )
    
    list_filter = (
        "created",
        "modified",
        "user__is_active",
        "user__is_staff"
        )

    readonly_fields = ("created", "modified")

class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users."""

    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"
