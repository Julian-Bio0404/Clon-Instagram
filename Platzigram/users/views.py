"""Users views."""

# Django
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView

# Forms
from users.forms import SignupForm

# Models
from posts.models import Post
from users.models import Profile, Follow


def login_view(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("posts:feed")
        else:
            return render(request, "users/login.html", {"error": "Invalid username and password"})
    return render(request, "users/login.html")


class SignupView(FormView):
    """Users sign up view."""

    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = "users/update_profile.html"
    model = Profile
    fields = ["website", "biography", "phone_number", "picture"]

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse("users:detail", kwargs={"username": username})


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = "users/detail.html"
    slug_field = "username"
    # slug_url_kwarg depende del nombre que le demos en la url de users Posts
    slug_url_kwarg = "username"
    queryset = User.objects.all()
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["posts"] = Post.objects.filter(user=user).order_by("-created")

         #conteo de publicaciones
        usr = Profile.objects.get(user=user) 
        usr.count_post = Post.objects.filter(user=user).count()
        usr.save()

        #  usr1=User.objects.get(username=usr)
        user_id=(User.objects.get(username=user)).id
        context['followers'] = Follow.objects.filter(following=user_id).count()
        context['following'] = Follow.objects.filter(follower=user_id).count()
       
        return context


@login_required
def follow_user(request,user1,user2):
    """current user= user2 , user to follow = user1 """

    user_id1=User.objects.get(username=user1).id
    user_id2=User.objects.get(username=user2).id

    if Follow.objects.filter(following=user_id1, follower=user_id2).count()!=0:
        Follow.objects.filter(following=user_id1, follower=user_id2).delete()
    else:
        Follow.objects.create(follower=user_id2,following=user_id1) 
  
    return HttpResponseRedirect(reverse('users:detail',args=[user1,]))
