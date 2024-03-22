from django.test import TestCase
from CriticCorner import models
from CriticCorner.models import Movie
from django.urls import reverse
class CategoryMethodTests(TestCase):
    def test_one(self):
        movie=Movie(api_id=11,title="AAA",genre="BBB",url="aaa.bbb.ccc",views=11,ratings=3,avg_rating=3.00000)
        movie.save()
        self.assertEqual(movie.api_id,11)
        self.assertEqual(movie.title,"AAA")
        self.assertEqual(movie.genre,"BBB")
        self.assertEqual(movie.url, "aaa.bbb.ccc")
        self.assertEqual(movie.views, 11)
        self.assertEqual(movie.ratings, 3)
        self.assertEqual(movie.avg_rating, 3.00000)


class IndexViewTests(TestCase):
    def testtwo(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def addmovie(api_id,title,genre,url,views,ratings,avg_rating):
        movie=Movie.y.objects.get_or_create(api_id=0)[0]
        movie.api_id=api_id
        movie.title=title
        movie.genre=genre
        movie.url=url
        movie.views=views
        movie.ratings=ratings
        movie.avg_rating=avg_rating







# Create your tests here.
