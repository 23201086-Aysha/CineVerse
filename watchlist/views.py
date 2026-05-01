from django.shortcuts import render, redirect
from .models import Watchlist
from django.contrib.auth.decorators import login_required


@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        movie_title = request.POST.get('movie_title')
        movie_image = request.POST.get('movie_image')
        user = request.user

        Watchlist.objects.get_or_create(user=user, movie_title=movie_title, movie_image=movie_image)

        return redirect('watchlist_view')  # Watchlist page-e niye jabe


@login_required
def watchlist_view(request):
    items = Watchlist.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'items': items})

# Create your views here.
