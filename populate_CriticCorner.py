import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'critic_corner.settings')
import random
import django
from django.core.files import File
from django.conf import settings
from urllib import request
django.setup()
import CriticCorner.models as models
from CriticCorner.helpers.TMBDactions import *

def populate():
    # Our Movie model is designed to only accept JSON responses 
    # From the TMDB API so our test data is also in this form.
    
    movies = [{'adult': False, 'backdrop_path': '/s9YTxwaByYeoSqugYjJJtZjMRAG.jpg', 'genre_ids': [28, 27, 35, 53], 'id': 1211483, 'original_language': 'en', 'original_title': 'Skal - Fight for Survival', 
               'overview': "My name's Arthur, a huge Internet star who's just hit 3 million subs. While in the midst of throwing an epic party to celebrate, the universe had the balls to bring on the effing apocalypse and cut my night short. What was supposed to be a perfect hangover, has turned into an epic fight for survival.", 
               'popularity': 404.1, 'poster_path': '/1On8iF3AsFIbpyfZg1xiGWMAFBn.jpg', 'release_date': '2023-11-24', 
               'title': 'Skal - Fight for Survival', 'video': False, 'vote_average': 5.5, 'vote_count': 51},
              {'adult': False, 'backdrop_path': None, 'genre_ids': [18, 53], 'id': 93782, 'original_language': 'en', 'original_title': 'Fate', 
               'overview': 'Serial killers have plagued the American landscape for decades, committing gruesome atrocities, and providing some tough cases for criminal investigators to crack. This thriller follows the travails of two detectives who are on the trail of a bizarre murderer intent on slaughtering his victims, then using them as real-life puppets in a tale that he is trying to tell. The plot holds a key to the whereabouts of the monstrous deviant, but the detectives have to unravel it quickly before more unsuspecting citizens become theater fodder for the unhinged madman.', 
               'popularity': 1.96, 'poster_path': '/3rIOyrU9I4xpUeYcLIM8hdZNJZU.jpg', 'release_date': '2003-03-15', 
               'title': 'Fate', 'video': False, 'vote_average': 2.0, 'vote_count': 1},
              {'adult': False, 'backdrop_path': '/jNsK2a8A1DYpaCX5HGElp3t4x6.jpg', 'genre_ids': [27, 28, 878], 'id': 56832, 'original_language': 'ja', 'original_title': 'Gantz', 
               'overview': 'After trying to rescue a man on the subway tracks, two teens wake up in a room dominated by a mysterious black sphere that sends them to hunt down and kill aliens hiding on Earth.', 
               'popularity': 18.159, 'poster_path': '/vScJdcqXHyupdeO3wkTqT92ew85.jpg', 'release_date': '2010-11-29', 
               'title': 'Gantz', 'video': False, 'vote_average': 6.606, 'vote_count': 282},
              {'adult': False, 'backdrop_path': '/8GXri7UnwE7dVNfUAZVDn7Z8UBZ.jpg', 'genre_ids': [12, 28, 37], 'id': 333484, 'original_language': 'en', 'original_title': 'The Magnificent Seven', 
               'overview': 'Looking to mine for gold, greedy industrialist Bartholomew Bogue seizes control of the Old West town of Rose Creek. With their lives in jeopardy, Emma Cullen and other desperate residents turn to bounty hunter Sam Chisolm for help. Chisolm recruits an eclectic group of gunslingers to take on Bogue and his ruthless henchmen. With a deadly showdown on the horizon, the seven mercenaries soon find themselves fighting for more than just money once the bullets start to fly.', 
               'popularity': 59.607, 'poster_path': '/ezcS78TIjgr85pVdaPDd2rSPVNs.jpg', 'release_date': '2016-09-14', 
               'title': 'The Magnificent Seven', 'video': False, 'vote_average': 6.428, 'vote_count': 5690},
              {'adult': False, 'backdrop_path': '/GZx3RAiTJAhXOdhLLyCAbqRl11.jpg', 'genre_ids': [37, 80, 18], 'id': 338766, 'original_language': 'en', 'original_title': 'Hell or High Water', 
               'overview': "A divorced dad and his ex-con brother resort to a desperate scheme in order to save their family's farm in West Texas.", 
               'popularity': 26.575, 'poster_path': '/ljRRxqy2aXIkIBXLmOVifcOR021.jpg', 'release_date': '2016-08-11', 
               'title': 'Hell or High Water', 'video': False, 'vote_average': 7.296, 'vote_count': 4255}
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
    
    def add_movie(movie_dict):
        mov_id = movie_dict["id"]
    
        genre = ",".join([get_genres_by_id(i) for i in movie_dict["genre_ids"]])
        url = get_trailer_url_by_id(mov_id)
        m = models.Movie.objects.get_or_create(api_id=mov_id,
                                        title= movie_dict["title"],
                                        genre=genre,
                                        url=url,)[0]
        m.ratings = 20
        m.avg_rating = float(random.randint(0,5))
        m.views = 60
    
        image_url = settings.ONLINE_IMAGE_ROOT + movie_dict["poster_path"]
        result = request.urlretrieve(image_url)
        
        m.poster.save(content=File(file=open(result[0], 'rb')), name=movie_dict["poster_path"][2:])
        m.save()
        return m
    
    def add_userProfile(username, email, password, phone_no):
        user = models.User.objects.get_or_create(username=username, email=email, password=password)[0]
        uP = models.UserProfile.objects.get_or_create(user=user, phone_number=phone_no)[0]
        uP.save()
        return uP
    def add_review(user, movie, content, rating):
        r = models.Review.objects.get_or_create(user=user, movie=movie, content=content, rating=rating)[0]
        r.save()
        return r
    
    def add_wishlist(user, movie):
        w = models.WishList.objects.get_or_create(user_profile=user, movie=movie)[0]
        w.save()
        return w
    
    movie_objects = []
    for movie in movies:
        movie_objects.append(add_movie(movie))

    userPobjects = []
    for i in range(len(user_profiles)):
        userPobjects.append(add_userProfile(users[i]['username'], users[i]['email'], users[i]['password'], user_profiles[i]['phone_number']))

    for i in range(len(reviews)):
        add_review(userPobjects[i % len(userPobjects)], movie_objects[i], reviews[i]['content'], reviews[i]['rating'])

    for userProfile in userPobjects:
        for i in range(2):
            add_wishlist(userProfile, random.choice(movie_objects))

    
if __name__ == "__main__":
    print('Starting Rango population script...')
    populate()