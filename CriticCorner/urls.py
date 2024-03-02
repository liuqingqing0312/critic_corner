from django.urls import path 
from CriticCorner import views

app_name = 'CriticCorner'

urlpatterns = [
    path('about/', views.about, name='about'),
]
