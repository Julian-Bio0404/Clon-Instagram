"""Posts views."""

# Django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User

# Forms
from posts.forms import PostForm, CommentForm

# Models
from posts.models import Post, Comment, Like
from users.models import Follow


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all posts published by following."""

    template_name = "posts/feed.html"
    ordering = ("-created")
    paginate_by = 30
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        follows = Follow.objects.filter(follower=user.pk)
        following = [follow.following for follow in follows]
        following.append(user.id)
        posts = Post.objects.filter(user__id__in=following)
        return posts


class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = "posts/detail.html"
    queryset = Post.objects.all()
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object()).all()
        context['form_comments'] = CommentForm()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    template_name = "posts/new.html"
    form_class = PostForm
    success_url = reverse_lazy("posts:feed")

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context


@login_required
def comment(request, pk=None):
    """Save or delete comments."""

    # Comentar
    if request.method == 'POST':
        post = {
            "user": request.user.id,
            "profile": request.user.id,
            "comment": request.POST["comment"],
            "post": request.POST["post"]
        }

        form = CommentForm(post)

        if form.is_valid():
            form.save()
            return redirect("posts:feed")

    # Eliminar comentario
    elif request.method == "GET":
        comment = Comment.objects.filter(pk=pk)
        comment.delete()
        return redirect("posts:feed")
    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)


def give_a_like(request, user, pk):
    """Like view.
    Allow you to like a post, 
    user=current user, pk=post.pk"""

    user = User.objects.get(username=user) 
    post_id = Post.objects.get(pk=pk)

    if Like.objects.filter(user=user, post=post_id).count() != 0:
        Like.objects.filter(user=user, post=post_id).delete()
    else:
        Like.objects.create(user=user, post=post_id)

    # Conteo de likes
    post = Post.objects.get(pk=pk)
    post.likes = Like.objects.filter(post=post).count()
    post.save()

    return redirect("posts:feed")


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Delete a post."""

    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("posts:feed")

    def get_object(self):
        obj = super().get_object()
        obj.delete()
