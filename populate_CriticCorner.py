import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'critic_corner.settings')
import random
import django
from django.core.files import File
from django.conf import settings

django.setup()
from CriticCorner.models import Movie, Review, UserProfile, User

def populate():
    movies = [{'title': "hound of winchester",
               'url': 'https://www.youtube.com/watch?v=xfsOSCeXOeA',
               'genre': Movie.HORROR},
               {'title': "count of transylvania",
               'url': 'https://www.youtube.com/watch?v=xfsOSCeXOeA',
               'genre': Movie.HORROR},
               {'title': "hound of loversville",
               'url': 'https://www.youtube.com/watch?v=xfsOSCeXOeA',
               'genre': Movie.ROMANCE},
               {'title': "hound of action",
               'url': 'https://www.youtube.com/watch?v=xfsOSCeXOeA',
               'genre': Movie.ACTION},
               ]

    users = [{'username': 'noobhunter23',
              'email': 'tobi@gmail.com',
              'password': 'secretpassword'},
             {'username': 'nathan101',
              'email': 'chungus@yahoo.com',
              'password': "theOneWhoKnocks"}]

    user_profiles = [{'phone_number': '07128917237'},
                     {'phone_number': '07234329428'},]
    
    reviews = [{'content': 'not great, would have like to see more explosions.',
                'rating': 2.2},
                {'content': 'amazing, this movie changed everything for me',
                'rating': 5.0},
                {'content': 'good fun movie to watch with the family',
                 'rating': 4.2}]
    
    image_paths = os.listdir(os.path.join(os.getcwd(), 'test_media'))
    
    def add_movie(title, url, genre):
        m = Movie.objects.get_or_create(url=url, title=title,genre=genre)[0]
        m.ratings = 20
        m.avg_rating = float(random.randint(0,5))
        m.views = 60
        cur_path = random.choice(image_paths)
        m.poster.save(content=File(file=open(os.path.join(os.getcwd(), 'test_media', cur_path), 'rb')), name=cur_path)
        m.save()
        return m
    def add_userProfile(username, email, password, phone_no):
        user = User.objects.get_or_create(username=username, email=email, password=password)[0]
        uP = UserProfile.objects.get_or_create(user=user, phone_number=phone_no)[0]
        uP.save()
        return uP
    def add_review(user, movie, content, rating):
        r = Review.objects.get_or_create(user=user, movie=movie, content=content, rating=rating)[0]
        r.save()
        return r
    
    movie_objects = []
    for movie in movies:
        movie_objects.append(add_movie(movie['title'], movie['url'], movie['genre']))

    userPobjects = []
    for i in range(len(user_profiles)):
        userPobjects.append(add_userProfile(users[i]['username'], users[i]['email'], users[i]['password'], user_profiles[i]['phone_number']))

    for i in range(len(reviews)):
        add_review(userPobjects[i % len(userPobjects)], movie_objects[i], reviews[i]['content'], reviews[i]['rating'])

    

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

