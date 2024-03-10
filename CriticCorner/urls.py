from django.urls import path 
from CriticCorner import views

app_name = 'CriticCorner'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('movie/<str:title>/', views.movie, name='movie'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_review/', views.add_review, name='add_review'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
