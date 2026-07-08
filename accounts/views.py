from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CustomUserRegistrationForm, CustomAuthenticationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                username=username,
                password=password,
            )

            if user:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.username}!"
                )

                return redirect("home")
    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")


@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user,
        },
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
                "Profile updated successfully."
            )

            return redirect("profile")
        
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )
