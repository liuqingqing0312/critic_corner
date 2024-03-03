from django.contrib import admin
from CriticCorner.models import Movie, UserProfile, Review

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','genre','url')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'rating')

admin.site.register(Movie,MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
