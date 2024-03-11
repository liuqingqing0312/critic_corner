from django.contrib import admin
from CriticCorner.models import Movie, UserProfile, Review, WishList

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','genre','url','slug')
    prepopulated_fields = {'slug':('title',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'rating')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'movie')
admin.site.register(Movie,MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
admin.site.register(WishList, WishlistAdmin)
