from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from CriticCorner.models import Movie, UserProfile, Review, WishList
from CriticCorner.forms import UserForm, UserProfileForm

def about(request):
    return render(request, 'CriticCorner/about.html')

def home(request):
    return render(request, 'CriticCorner/home.html')

def activate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse("Your CriticCorner account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'CriticCorner/login.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'CriticCorner/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('CriticCorner:home'))

def contact(request):
    return render(request, 'CriticCorner/contact.html')

def movie(request):
    return render(request, 'CriticCorner/movie.html')

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishList.objects.filter(user_profile=request.user.userprofile)
        return render(request, 'CriticCorner/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return render(request, 'CriticCorner/wishlist.html', {'wishlist_items': []})