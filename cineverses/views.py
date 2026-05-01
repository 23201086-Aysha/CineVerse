from django.shortcuts import redirect, render
from movie_app.models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html",{"movies": movies})