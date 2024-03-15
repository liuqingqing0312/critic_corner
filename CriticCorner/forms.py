from django import forms
from django.contrib.auth.models import User
from CriticCorner.models import Movie, UserProfile, Review, WishList

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'picture',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        labels = {
            'content': 'Review',
            'rating': 'Rating (out of 5)',
        }
        
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'