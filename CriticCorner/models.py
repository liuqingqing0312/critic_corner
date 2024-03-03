from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


MIN_RATING_VALUE = 0
MAX_RATING_VALUE = 5

# Create your models here.

class Movie(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    HORROR = 'horror'
    ROMANCE = 'romance'
    ACTION = 'action'
    COMEDY = 'comedy'

    GENRE_CHOICES = [
        (HORROR, 'Horror'),
        (ROMANCE, 'Romance'),
        (ACTION, 'Action'),
        (COMEDY, 'Comedy'),
        # Add more genres here if needed
    ]
    
    MIN_RATING_VALUE = 0
    MAX_RATING_VALUE = 5
    title = models.CharField(max_length=256)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    views = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    poster = models.ImageField(upload_to = 'posters/')
    release_date = models.DateField()
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(MIN_RATING_VALUE), MaxValueValidator(MAX_RATING_VALUE)])
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)

    def __str__(self):
        return self.title


class UserProfile(User):
    phone_number = models.CharField(max_length=15, blank=False)
    wishlist = models.ManyToManyField(Movie, related_name='wishlisted_by', blank=True)

    def __str__(self):
        return self.username


class Review(models.Model):
    user = models.ForeignKey(UserProfile,related_name='writes', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='written_about',on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(MIN_RATING_VALUE), MaxValueValidator(MAX_RATING_VALUE)])

    def __str__(self):
        return self.user.__str__() + self.movie.__str__()
    


