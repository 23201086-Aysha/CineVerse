from django.db import models
from django.contrib.auth.models import User
from movie_app.models import Movie

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    is_spoiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)