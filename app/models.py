from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    actors = models.ManyToManyField('Actor')
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    is_top = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # ДОБАВЬ ЭТОТ МЕТОД
    def average_rating(self):
        reviews = self.reviews.filter(is_active=True)
        if reviews.exists():
            total = sum([review.rating for review in reviews])
            return round(total / reviews.count(), 1)
        return 0


class Director(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='directors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author_name} - {self.movie.title}"