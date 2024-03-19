#tmdb wrapper is used wherever possible but some things have to be done with raw requests.
from tmdbv3api import Movie, TMDb, Genre
from datetime import datetime, timedelta
from django.utils.text import slugify
import CriticCorner.models as models
import json
import requests
from django.core.files import File
import random
from django.conf import settings
from urllib import request
from typing import Optional

API_KEY = "e359feb309aff2209a6cfea5553838bf"
MAX_NUM_PAGES_TO_LOAD = 10

movie = Movie()
movie.api_key = API_KEY

genre = Genre()
genre.api_key = API_KEY
raw_genre_data = genre.movie_list()["genres"]
genres = {raw_genre_data[i]["id"]: raw_genre_data[i]["name"] for i in range(len(raw_genre_data))}

def get_movies_by_search(query: str) -> list:
    """uses the TMBD api to find results related to the query

    Args:
        query (str): search string entered by user

    Returns:
        list: list in order of relevance consisting of all relevant movies to the query. Empty if no movies found
    """
    related = movie.search(query)
    
    if len(related.get("results")) == 0:
        return []
    
    return [mov for mov in related]

def get_genres_by_id(id: int) -> str:
    """"""
    if id in genres:
        return genres[id]
    else:
        return "No such genre id"

def get_trailer_url_by_id(id: int) -> str:
    """returns youtube video url."""
    video_object = [chungus for chungus in movie.videos(id)][0]
    # if no proper results then return early
    if len(video_object)< 6:
        return "https://www.youtube.com/embed/ihyjXd2C-E8"
    return "https://www.youtube.com/embed/"+dict(video_object)["key"]

def advanced_movie_search(title: str) -> list:
    """
    returns list of dictionaries of max length MAX_NUM_PAGES_TO_LOAD*20. keep it stored in memory so we are not making 
    unneccessary requests to api. differs from get_movies_by_search as it loads more than just the first page
    """

    #first we must find the number of pages that the search generates. This means searching for the title
    results = movie.search(title)

    # if title does not match anything in table
    if results.get("total_results") == 0:
        return []
    
    num_pages = results.get("total_pages")

    params = {
        'query': title,
        'api_key': API_KEY,
        'page' : 1
    }

    movies = []
    for i in range(min(num_pages, MAX_NUM_PAGES_TO_LOAD)):
        response = requests.get('https://api.themoviedb.org/3/search/movie', params=params)
        if not(response.ok):
            return movies
        results = json.loads(response.content)["results"]
        #append new movie dicts to our list
        movies += results

        #increase page number so next request is on next page
        params["page"] += 1

    return movies

def movie_json_to_movie_object(movie_dict: dict) -> models.Movie:
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
def advanced_movie_search_sorted_by_popularity(title: str) -> list:
    movies = advanced_movie_search(title)
    sorted_movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)
    return sorted_movies

def advanced_movie_search_sorted_by_release(title: str) -> list:
    """
    Searches for movies based on the title using advanced search and then sorts
    the resulting list by release date.
    """
    # Call advanced_movie_search to get the list of movies
    movies = advanced_movie_search(title)

    # Sort the movies by release date if 'release_date' is present in each movie dictionary
    sorted_movies = sorted(movies, key=lambda x: x.get('release_date', ''), reverse=True)

    return sorted_movies


def get_genres() -> dict:
    return genres



if __name__ == "__main__":
    #test script
    # print(len(get_movies_by_search("and")))
    # print(get_trailer_url_by_id(93782))
    # print(get_genres())
    
    # print(advanced_movie_search("life"))
    print(advanced_movie_search_sorted_by_release("life"))
