from django.shortcuts import redirect, render


def home(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")