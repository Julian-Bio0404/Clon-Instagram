"""Posts URLs."""

# Django
from django.urls import path

# Views
from posts import views


urlpatterns = [

    path(
        route="",
        view=views.PostsFeedView.as_view(), 
        name="feed"
    ),

    path(
        route="posts/new/",
        view=views.CreatePostView.as_view(), 
        name="create"
    ),

    path(
        route="posts/<int:pk>",
        view=views.PostDetailView.as_view(),
        name="detail"
    ),

    path(
        route="posts/delete/<int:pk>",
        view=views.DeletePostView.as_view(),
        name="delete"
    ),

    path(
        route="<str:user>/<int:pk>/", 
        view=views.give_a_like,
        name="like"
    ),

    path(
        route="posts/save_comment",
        view=views.comment,
        name="save_comment"
    ),

    path(
        route="posts/delete_comment/<int:pk>",
        view=views.comment,
        name="delete_comment"
    ),
]