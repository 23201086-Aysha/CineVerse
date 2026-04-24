from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout, authenticate, login


# user registration view
def register_user(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # check pass & confirm pass
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('user:register_user')

        # check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('user:register_user')

        # create user
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = False  # Cannot access admin
        user.is_superuser = False  # Definitely not admin
        user.save()

        # register done msg
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('user:login_user')

        # render reg form for GET method
    return render(request, 'user/register_form.html')


# login view
def login_user(request):
    if request.method == "POST":
        # get data from form
        username = request.POST.get("username")
        password = request.POST.get("password")
        # if no user, return none
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # no login msg
            messages.error(request, "Invalid credentials")
            return render(request, "user/login_form.html")
    else:
        return render(request, "user/login_form.html")

# logout view
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

