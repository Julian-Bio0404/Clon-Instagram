"""Users views."""

# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    """Login view."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect("feed")
        else:
            return render(request, "users/login.html", {"error": "Invalid username and password"})
    return render(request, "users/login.html")