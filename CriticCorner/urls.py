from django.urls import path 
from CriticCorner import views

app_name = 'CriticCorner'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.activate, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('movie/', views.movie, name='movie'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
