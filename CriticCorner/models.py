from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import datetime
from django import utils
import glob
from django.template.defaultfilters import slugify
from six import python_2_unicode_compatible


MIN_RATING_VALUE = 0
MAX_RATING_VALUE = 5

# Create your models here.
class Movie(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    MIN_RATING_VALUE = 0
    MAX_RATING_VALUE = 5
    
    #the id that is used by TMBD api to identify a specific movie
    api_id = models.IntegerField(primary_key=True, default=0)
    title = models.CharField(max_length=256)
    genre = models.CharField(max_length=1000)
    
    # url will contain link to youtube video
    url = models.URLField(max_length=URL_MAX_LENGTH)
    views = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    poster = models.ImageField(upload_to = 'media/posters')
    release_date = models.DateField(default=utils.timezone.now)
    avg_rating = models.DecimalField(max_digits=20, decimal_places=10, default=0.0, validators=[MinValueValidator(MIN_RATING_VALUE), MaxValueValidator(MAX_RATING_VALUE)])
    slug = models.SlugField(unique=True)
    
    # will have to later check to remove entries from database that
    # are > 6months old, this will happen once every 2 months
    date_added = models.DateField(default=utils.timezone.now)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + str(self.release_date)[:10])
        super(Movie, self).save(*args, **kwargs)

    def get_genre(self):
        genre_list = self.genre.split(",")
        return genre_list
        
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=False)
    picture = models.ImageField(upload_to='media/pfps', default='test_media/R.jpeg')

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(UserProfile,related_name='writes', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='written_about',on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(MIN_RATING_VALUE), MaxValueValidator(MAX_RATING_VALUE)])

    def __str__(self):
        return self.user.__str__() + self.movie.__str__()
    
class WishList(models.Model):
    user_profile = models.ForeignKey(UserProfile,related_name='has', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='contains',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_profile.__str__() + self.movie.__str__()


