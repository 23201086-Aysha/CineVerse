from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre
from review.models import Review


#  Home
@login_required
def home(request):
    return redirect('movie_app:movie_list')


#  Movie List
@login_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


#  Movie Detail
@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'reviews': reviews
    })


#  Add Movie
@login_required
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
            return redirect('movie_app:movie_list')

    return render(request, 'add_movie.html', {'genres': genres})


#  Edit Movie
@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = Genre.objects.all()

    if request.method == "POST":
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_date = request.POST.get('release_date')
        movie.genre_id = request.POST.get('genre')

        movie.save()
        return redirect('movie_app:movie_detail', pk=movie.pk)

    return render(request, 'edit_movie.html', {
        'movie': movie,
        'genres': genres
    })


#  Delete Movie
@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        movie.delete()
        return redirect('movie_app:movie_list')

    return render(request, 'delete_movie.html', {'movie': movie})


#  Genre List
@login_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})


#  All Reviews
@login_required
def all_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'all_reviews.html', {'reviews': reviews})


#  My Reviews
@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'my_reviews.html', {'reviews': reviews})


#  Add Review
@login_required
def add_review(request):
    movies = Movie.objects.all()

    if request.method == "POST":
        movie_id = request.POST.get('movie')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if movie_id and rating:
            Review.objects.create(
                user=request.user,
                movie_id=movie_id,
                rating=rating,
                comment=comment
            )
            return redirect('movie_app:all_reviews')

    return render(request, 'add_review.html', {'movies': movies})


#  Top Reviews
@login_required
def top_reviews(request):
    reviews = Review.objects.order_by('-rating')[:10]
    return render(request, 'top_reviews.html', {'reviews': reviews})