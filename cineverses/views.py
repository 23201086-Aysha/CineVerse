from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect("user:login_user")