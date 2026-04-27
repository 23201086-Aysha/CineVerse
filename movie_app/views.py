from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre


# Add Movie
def add_movie(request):
    genres = Genre.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        genre_id = request.POST.get('genre')

        if title and genre_id:
            Movie.objects.create(
                title=title,
                description=description,
                release_date=release_date,
                genre_id=genre_id
            )
            return redirect('movie_list')

    return render(request, 'movie/add_movie.html', {'genres': genres})


# Edit Movie
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = Genre.objects.all()

    if request.method == "POST":
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_date = request.POST.get('release_date')
        movie.genre_id = request.POST.get('genre')

        movie.save()
        return redirect('movie_detail', pk=movie.pk)

    return render(request, 'movie/edit_movie.html', {
        'movie': movie,
        'genres': genres
    })


# Delete Movie
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movie/delete_movie.html', {'movie': movie})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie/movie_detail.html', {'movie': movie})