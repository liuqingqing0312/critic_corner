from audioop import avg, avgpp
import json
import os
from urllib.parse import unquote_plus
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
import requests
from urllib import request as req
from django.core.files import File
from CriticCorner.models import Movie, UserProfile, Review, WishList
from CriticCorner.forms import UserForm, UserProfileForm, ReviewForm, MovieForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from CriticCorner.helpers.TMBDactions import advanced_movie_search, get_genres, get_trailer_url_by_id, get_genres_by_id
from django.template.defaultfilters import slugify

def about(request):
    return render(request, "CriticCorner/about.html")


def home(request):
    # Retrieve popular, new released, and top-rated movies from the database
    popular_movies = Movie.objects.order_by('views')[:5]  # Adjust this filter based on your criteria
    new_released_movies = Movie.objects.order_by('-release_date')[:5]
    top_rated_movies = Movie.objects.order_by('-avg_rating')[:5]

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

    # When called from search it will be a post request because there is a chance the movie doesnt exist yet
    if request.method == "POST":
        # We have recieved the post
        if movie == None:
            # Movie not in database, we have to add it
            form = MovieForm(request.POST)
            if form.is_valid():
                # Now add all the neccessary details before we can submit
                movie = form.save(commit=False)
                url = get_trailer_url_by_id(movie.api_id)
                poster_path = form.cleaned_data["poster_path"]
                image_url = settings.ONLINE_IMAGE_ROOT + poster_path
                result = req.urlretrieve(image_url)
                
                movie.poster.save(content=File(file=open(result[0], 'rb')), name=poster_path[2:])
                movie.url = url
                print(type(json.loads(movie.genre)))
                movie.genre = ",".join([get_genres_by_id(id) for id in json.loads(movie.genre)])
                movie.save()

                
            else:
                print(form.errors)


    reviews = Review.objects.filter(movie=movie)
    reviews_count = reviews.count()
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / reviews.count() if reviews.count() > 0 else 0
    return render(request, 'CriticCorner/movie.html', {'movie': movie, 'reviews': reviews, 'average_rating': average_rating, 'reviews_count': reviews_count})

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
        # https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average#:~:text=I%20want%20to%20add%20a%20value%20to%20an,d%20s%20i%20z%20e%20n%20e%20w
        # see above for explanation
        new_avg_rating = movie.avg_rating + ((float(review.rating) - float(movie.avg_rating))/movie.ratings) 
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

    movies = advanced_movie_search(query)
    
    for movie in movies:
        movie["slug"] = slugify(movie["title"] + str(movie.get("release_date", ""))[:10])
    

    return render(request, "CriticCorner/search.html", {"movies": movies,
                                                        "query": query,
                                                        "genres": get_genres()})

def add_movie(request):
    if request.method == "POST":
        data = json.loads(request.body)
        movies_data = data.get("movies")
        if movies_data:
            for movie_data in movies_data:
                # Here, you would extract relevant information from the movie data
                # and create a new Movie object in the database
                movie = Movie.objects.create(
                    title=movie_data.get("title"),
                    genre=movie_data.get("genre"),
                    # Add more fields as necessary
                )
                # Assuming you have fields like 'slug' and 'poster_path' in movie_data,
                # you can set them accordingly as well

                # Save the movie to the database
                movie.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "No movie data provided"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)