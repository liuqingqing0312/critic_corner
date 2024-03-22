from django.test import TestCase, Client, override_settings
from CriticCorner import models
from CriticCorner.models import *
from django.urls import reverse
from django import utils
from datetime import date

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get_or_create(username='testuser', password='Testpassword1')[0]
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.phone_number = "07498578674"
        self.user_profile.save()
        
        self.movie = Movie.objects.create(
            api_id=1,
            title='Test Movie',
            genre='Action, Comedy',
            url='https://example.com/trailer',
            poster='path/to/poster.jpg',
        )

    def test_home_view(self):
        response = self.client.get(reverse('CriticCorner:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CriticCorner/home.html')

    def test_movie_view(self):
        response = self.client.get(reverse('CriticCorner:movie', args=[self.movie.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CriticCorner/movie.html')
        
    def test_add_wishlist_view_unauthenticated(self):
        self.client.logout()
        
        data = {
            'title': self.movie.title,
            'content': "we like fortntie lul",
            'rating': 2.3
        }
        response = self.client.post(reverse('CriticCorner:add_wishlist'), data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('auth_login') + '?next=' + reverse('CriticCorner:add_wishlist'))
        self.assertEqual(WishList.objects.count(), 0)
        
    def test_add_wishlist_view(self):
        self.client.force_login(self.user)
        data = {
            'title': self.movie.title
        }
        response = self.client.post(reverse('CriticCorner:add_wishlist'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful wishlist addition
        self.assertEqual(WishList.objects.count(), 1)
        wishlist_item = WishList.objects.first()
        self.assertEqual(wishlist_item.user_profile, self.user_profile)
        self.assertEqual(wishlist_item.movie, self.movie)

    def test_add_review_view_unauthenticated(self):
        self.client.logout()
        
        data = {
            'content': 'This is a test review',
            'rating': 4.5,
            'title': self.movie.title
        }
        response = self.client.post(reverse('CriticCorner:add_review'), data)
        self.assertEqual(response.status_code, 302)  # unauthenticated users are redirected
        self.assertRedirects(response, reverse('auth_login') + '?next=' + reverse('CriticCorner:add_review'))
        self.assertEqual(Review.objects.count(), 0)

    def test_add_review_view(self):
        self.client.force_login(self.user)
        data = {
            'content': 'This is a test review',
            'rating': 4.5,
            'title': self.movie.title
        }
        response = self.client.post(reverse('CriticCorner:add_review'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful review
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.content, data['content'])
        self.assertEqual(review.rating, data['rating'])
        self.assertEqual(review.movie, self.movie)
        self.assertEqual(review.user, self.user_profile)

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.get_or_create(username='testuser', password='Testpassword1')[0]
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.phone_number = "07498578674"
        self.user_profile.save()
        
        self.movie = Movie.objects.create(
            api_id=1,
            title='Test Movie',
            genre='Action,Comedy',
            url='https://example.com/trailer',
            poster='path/to/poster.jpg',
            release_date=date(2023, 1, 1)
        )

    def test_movie_model(self):
        self.assertEqual(str(self.movie), self.movie.title)
        genres = self.movie.get_genre()
        self.assertListEqual(genres, ['Action', 'Comedy'])

    def test_userprofile_model(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_review_model(self):
        review = Review.objects.create(
            user=self.user_profile,
            movie=self.movie,
            content='This is a test review',
            rating=4.5
        )
        self.assertEqual(str(review), f'{self.user.username}{self.movie.title}')

    def test_wishlist_model(self):
        wishlist_item = WishList.objects.create(
            user_profile=self.user_profile,
            movie=self.movie
        )
        self.assertEqual(str(wishlist_item), f'{self.user.username}{self.movie.title}')





