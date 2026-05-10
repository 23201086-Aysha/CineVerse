from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=True)

    def __str__(self):
        return self.title