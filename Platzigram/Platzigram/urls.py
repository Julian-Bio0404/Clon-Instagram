"""Platzigram URLs module."""

# Django
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

# Views
from Platzigram import views as local_views
from posts import views as posts_views
from users import views as users_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path("hello-world/", local_views.hello_world, name="hello_worlds"),
    path("posts/", posts_views.list_posts, name="feed"),
    path("users/login/", users_views.login_view, name="login" ),
    path("users/logout/", users_views.logout_view, name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
