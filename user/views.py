from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CineUser


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
            if user.is_superuser or user.is_staff:
                messages.error(request, "Admin accounts must use the admin panel.")
                return redirect("user:login_user")
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


# profile view
@login_required
def user_profile(request):
    profile, _ = CineUser.objects.get_or_create(user=request.user)
    return render(request, 'user/user_profile.html', {'profile': profile})

# update profile
@login_required
def update_user(request):
    user = request.user
    profile, _ = CineUser.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username:
            messages.error(request, 'Username is required.')
            return redirect('user:update_profile')

        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('user:update_profile')

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('user:user_profile')

    return render(request, 'user/update_profile.html', {
        'user': user,
        'profile': profile
    })