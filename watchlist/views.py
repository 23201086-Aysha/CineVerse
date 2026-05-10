from django.shortcuts import render, redirect, get_object_or_404
from .models import Watchlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        movie_title = request.POST.get('movie_title')
        movie_image = request.POST.get('movie_image')
        user = request.user

        watchlist_item, created = Watchlist.objects.get_or_create(user=user, movie_title=movie_title, movie_image=movie_image)

        if created:
            messages.success(request, f'"{movie_title}" has been added to your watchlist!')
        else:
            messages.info(request, f'"{movie_title}" is already in your watchlist.')

        return redirect('watchlist:watchlist_view')  # Watchlist page-e niye jabe
    else:
        return redirect ('movie_app:movie_list')


@login_required
def watchlist_view(request):
    items = Watchlist.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'items': items})

@login_required
def remove_from_watchlist(request, item_id):
    item = get_object_or_404(Watchlist, id=item_id, user=request.user)
    movie_title = item.movie_title
    item.delete()
    messages.success(request, f'"{movie_title}" has been removed from your watchlist.')
    return redirect('watchlist:watchlist_view')
