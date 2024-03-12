from audioop import avg
from urllib.parse import unquote_plus
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from CriticCorner.models import Movie, UserProfile, Review, WishList
from CriticCorner.forms import UserForm, UserProfileForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def about(request):
    return render(request, 'CriticCorner/about.html')

def home(request):
    movies = Movie.objects.all()
    return render(request, 'CriticCorner/home.html', {'movies': movies})

def contact(request):
    return render(request, 'CriticCorner/contact.html')

def search(request):
    return render(request, 'CriticCorner/search.html')
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
        movie_title = request.POST.get('title')  # Retrieve movie title from form data
        
        # Check if movie_title is not None
        if movie_title is not None:
            # Decode the movie title
            decoded_title = unquote_plus(movie_title)
            
            # Retrieve the movie object based on the decoded title
            try:
                movie = Movie.objects.get(title=decoded_title)
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
            
            # Redirect to the movie page
            return redirect('CriticCorner:movie', slug=movie.slug)
        else:
            # Handle the case where movie_title is None
            return HttpResponse("Movie title is missing")
    else:
        # Handle GET requests if needed
        pass

@login_required
def add_wishlist(request):
    if request.method == 'POST':
        user = request.user
        movie_id = request.POST.get('movie')
        
        # Retrieve user profile
        user_profile = get_object_or_404(UserProfile, user=user)
        
        # Get the movie object
        movie = get_object_or_404(Movie, pk=movie_id)
        
        # Check if the movie is already in the user's wishlist
        if WishList.objects.filter(user_profile=user_profile, movie=movie).exists():
            # Optionally, you can provide feedback that the movie is already in the wishlist
            return redirect('CriticCorner:wishlist')  # Redirect to home or wherever you want
            
        # Add the movie to the user's wishlist
        wishlist_item = WishList.objects.create(user_profile=user_profile, movie=movie)
        
        # Optionally, you can provide feedback that the movie has been added to the wishlist
        # Redirect to the wishlist with the movie's slug
        return redirect('CriticCorner:wishlist')
    else:
        # Handle GET request (display wishlist or redirect to home)
        return redirect('CriticCorner:home')  # Redirect to home or wherever you want
        
@login_required
def remove_from_wishlist(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        # Assuming you have a user profile associated with the logged-in user
        user_profile = request.user.userprofile
        # Retrieve the movie from the wishlist and delete it
        wishlist_item = get_object_or_404(WishList, user_profile=user_profile, movie_id=movie_id)
        wishlist_item.delete()
    return redirect('CriticCorner:wishlist')

@login_required
def review_restrict(request):
    return render(request, 'CriticCorner/review_restrict.html')
