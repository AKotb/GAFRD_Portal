# users/views.py

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import CustomUserCreationForm


def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method != "POST":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
