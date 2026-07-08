from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    CustomAuthenticationForm,
    CustomUserRegistrationForm,
    ProfileForm,
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully! Please log in.",
            )

            return redirect("login")

    else:

        form = CustomUserRegistrationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/register.html",
        context,
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CustomAuthenticationForm(
        request,
        data=request.POST or None,
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!",
            )

            return redirect("home")

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/login.html",
        context,
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("home")


@login_required
def profile_view(request):

    return render(
        request,
        "accounts/profile.html",
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user,
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/edit_profile.html",
        context,
    )