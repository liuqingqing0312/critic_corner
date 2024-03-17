from tmdbv3api import Movie, TMDb, Genre
from datetime import datetime, timedelta
from django.utils.text import slugify
import json

API_KEY = "e359feb309aff2209a6cfea5553838bf"

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
    
def get_genres() -> dict:
    return genres
# you should never need to get movie info from database since if you have id
# you would also have all other relevant info stored locally
if __name__ == "__main__":
    #test script
    # print(get_movies_by_search("chungus"))
    print(get_movies_by_search("kungfu panda"))