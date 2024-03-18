from audioop import avg, avgpp
import os
from urllib.parse import unquote_plus
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
import requests
from CriticCorner.models import Movie, UserProfile, Review, WishList
from CriticCorner.forms import UserForm, UserProfileForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from CriticCorner.helpers.TMBDactions import advanced_movie_search, advanced_movie_search_sorted_by_popularity, advanced_movie_search_sorted_by_release

def about(request):
    return render(request, "CriticCorner/about.html")


def home(request):
    # Retrieve popular, new released, and top-rated movies from the database
    popular_movies = Movie.objects.order_by('views')  # Adjust this filter based on your criteria
    new_released_movies = Movie.objects.order_by('-release_date')
    top_rated_movies = Movie.objects.order_by('-avg_rating')

    # Pass the movie data to the template context
    context = {
        'popular_movies': popular_movies,
        'new_released_movies': new_released_movies,
        'top_rated_movies': top_rated_movies,
    }

    # Render the homepage template with the movie data
    return render(request, 'CriticCorner/home.html', context)

def contact(request):
    return render(request, 'CriticCorner/contact.html')

def movie(request, slug):
    movie = Movie.objects.filter(slug=slug).first()
    reviews = Review.objects.filter(movie=movie)
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / reviews.count() if reviews.count() > 0 else 0
    return render(request, 'CriticCorner/movie.html', {'movie': movie, 'reviews': reviews, 'average_rating': average_rating})

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()
        
@login_required
def wishlist(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            wishlist_items = WishList.objects.filter(user_profile=user_profile)
        except UserProfile.DoesNotExist:
            wishlist_items = []  # Handle the case where the user profile does not exist
        return render(request, 'CriticCorner/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return render(request, 'CriticCorner/wishlist.html', {'wishlist_items': []})

@login_required
def add_review(request):
    if request.method == 'POST':
        # Get form data
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        title = request.POST.get('title')  # Retrieve movie title from form data
        
        try:
            movie = Movie.objects.get(title=title)
        except Movie.DoesNotExist:
            # Handle the case where the movie doesn't exist
            # Redirect or display an error message
            return HttpResponse("Movie not found")

        # Check if the user has already reviewed this movie
        existing_review = Review.objects.filter(user=request.user.userprofile, movie=movie).first()
        if existing_review:
            # Optionally, you can provide feedback that the user has already reviewed this movie
            return redirect('CriticCorner:review_restrict')

        # Create review object with movie object
        review = Review.objects.create(
            user=request.user.userprofile,  # Assuming user is authenticated
            content=content,
            rating=rating,
            movie=movie  # Assign movie object to review
        )

        # Calculate the new average rating
        new_avg_rating = Review.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
        print("New Average Rating:", new_avg_rating)

        # Update the movie's average rating
        movie.avg_rating = new_avg_rating
        movie.save()
        print("Updated Average Rating:", movie.avg_rating)
        
        # Redirect to the movie page
        return redirect('CriticCorner:movie', slug=movie.slug)
    else:
        # Handle GET requests if needed
        pass

@login_required
def add_wishlist(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')  # Retrieve movie title from form data
        
        # Retrieve user profile
        user_profile = get_object_or_404(UserProfile, user=user)
        
        # Get the movie object using the title
        movie = get_object_or_404(Movie, title=title)
        
        # Check if the movie is already in the user's wishlist
        if WishList.objects.filter(user_profile=user_profile, movie=movie).exists():
            # Optionally, you can provide feedback that the movie is already in the wishlist
            return redirect('CriticCorner:wishlist')  # Redirect to wishlist or wherever you want
            
        # Add the movie to the user's wishlist
        wishlist_item = WishList.objects.create(user_profile=user_profile, movie=movie)
        
        # Optionally, you can provide feedback that the movie has been added to the wishlist
        # Redirect to the wishlist
        return redirect('CriticCorner:wishlist')
    else:
        # Handle GET request (display wishlist or redirect to home)
        return redirect('CriticCorner:home')  # Redirect to home or wherever you want
        
@login_required
def remove_from_wishlist(request):
    if request.method == 'POST':
        id = request.POST.get('id')  # Retrieve movie ID from form data
        
        if id:
            # Assuming you have a user profile associated with the logged-in user
            user_profile = request.user.userprofile
            # Retrieve the movie from the wishlist and delete it
            wishlist_item = WishList.objects.get(user_profile=user_profile, id=id)
            wishlist_item.delete()
    return redirect('CriticCorner:wishlist')

@login_required
def review_restrict(request):
    return render(request, 'CriticCorner/review_restrict.html')


@login_required
def account_view(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        user_reviews = Review.objects.filter(user=profile)
        user_wishlist = WishList.objects.filter(user_profile=profile)
    except UserProfile.DoesNotExist:
        profile = None
        user_reviews = []
        user_wishlist = []

    return render(request, "CriticCorner/account.html", {"user": user, "profile": profile, "user_reviews": user_reviews, "user_wishlist": user_wishlist})


def search_view(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "default")  # Get the sorting option

    # Fetch movies for each sorting option
    movies_popularity = advanced_movie_search_sorted_by_popularity(query)
    movies_release = advanced_movie_search_sorted_by_release(query)
    movies_default = advanced_movie_search(query)

    return render(request, "CriticCorner/search.html", {"movies_popularity": movies_popularity,
                                                        "movies_release": movies_release,
                                                        "movies_default": movies_default,
                                                        "query": query,
                                                        "sort_by": sort_by})
