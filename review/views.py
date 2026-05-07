from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewReply
from movie_app.models import Movie
from subscription.models import UserSubscription


def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)

    return render(request, 'review.html', {
        'movie': movie,
        'reviews': reviews
    })


# review add
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Check subscription limits
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    has_unlimited_reviews = user_subscription and user_subscription.has_feature('unlimited_reviews')

    if not has_unlimited_reviews:
        # Free users limited to 5 reviews per month
        from django.utils import timezone
        from datetime import timedelta
        month_ago = timezone.now() - timedelta(days=30)
        review_count = Review.objects.filter(user=request.user, created_at__gte=month_ago).count()
        if review_count >= 5:
            messages.error(request, "Free users are limited to 5 reviews per month. Upgrade to Basic or Premium for unlimited reviews.")
            return redirect('movie_reviews', movie_id=movie.id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        is_spoiler = request.POST.get('is_spoiler') == 'on'

        Review.objects.create(
            user=request.user,
            movie=movie,
            rating=rating,
            comment=comment,
            is_spoiler=is_spoiler
        )
        messages.success(request, "Review added successfully!")

    return redirect('movie_reviews', movie_id=movie.id)


# reply add
@login_required
def add_reply(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')

        ReviewReply.objects.create(
            review=review,
            user=request.user,
            reply_text=reply_text
        )

    return redirect('movie_reviews', movie_id=review.movie.id)


# review delete
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        review.delete()

    return redirect('movie_reviews', movie_id=review.movie.id)