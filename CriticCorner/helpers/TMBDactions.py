from tmdbv3api import Movie, TMDb, Genre
from datetime import datetime, timedelta
from django.utils.text import slugify

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

def get_genres_by_id(ids: list) -> str:
    """"""
    genre_names = []
    for id in ids:
        if id in genres:
            genre_names.append(genres[id])
        else:
            return "No such genre"
    return ', '.join(genre_names)

def get_trailer_url_by_id(id: int) -> str:
    """returns youtube video url."""
    return "https://www.youtube.com/embed/"+dict([chungus for chungus in movie.videos(id)][0])["key"]

def get_most_popular_movies() -> list:
    """Returns a list of dictionaries containing information about the most popular movies.

    Returns:
        list: List of dictionaries containing information about the most popular movies.
    """
    popular_movies = movie.popular()

    if len(popular_movies) == 0:
        return []

    # Extracting relevant information from each movie object
    popular_movies_info = []
    for movie_obj in popular_movies:
        movie_info = {
            'title': movie_obj.title,
            'slug': slugify(movie_obj.title),
            'poster_path': movie_obj.poster_path,
        }
        popular_movies_info.append(movie_info)

    return popular_movies_info

def get_newly_released_movies() -> list:
    """Returns a list of dictionaries containing information about the newly released movies.

    Returns:
        list: List of dictionaries containing information about the newly released movies.
    """
    # Initialize TMDb API
    tmdb = TMDb()
    tmdb.api_key = API_KEY

    # Initialize Movie object
    movie = Movie()

    # Define the start and end date range for the search (e.g., within the last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Get movies currently playing in theaters
    now_playing_movies = movie.now_playing()

    # Filter newly released movies within the specified date range
    new_movies = [movie_obj for movie_obj in now_playing_movies if start_date <= datetime.strptime(movie_obj.release_date, '%Y-%m-%d') <= end_date]

    # Sort new movies by release date
    new_movies.sort(key=lambda x: x.release_date, reverse=True)

    # Extract information for newly released movies
    newly_released_movies_info = []
    for movie_obj in new_movies:
        movie_info = {
            'title': movie_obj.title,
            'slug': slugify(movie_obj.title),
            'poster_path': movie_obj.poster_path,
        }
        newly_released_movies_info.append(movie_info)

    return newly_released_movies_info

def get_top_rated_movies() -> list:
    """Returns a list of dictionaries containing information about the top 10 rated movies.

    Returns:
        list: List of dictionaries containing information about the top 10 rated movies.
    """
    # Initialize TMDb API
    tmdb = TMDb()
    tmdb.api_key = API_KEY

    # Initialize Movie object
    movie = Movie()

    # Get top rated movies
    top_rated_movies = movie.top_rated()

    # Extract information for top 10 rated movies
    top_rated_movies_info = []
    for movie_obj in top_rated_movies:
        movie_info = { 
            'title': movie_obj.title,
            'slug': slugify(movie_obj.title),
            'poster_path': movie_obj.poster_path,
        }
        top_rated_movies_info.append(movie_info)

    return top_rated_movies_info

def get_movie_details(slug):
    """Fetches movie details from TMDb based on the provided slug.

    Args:
        slug (str): The slug of the movie.

    Returns:
        dict: A dictionary containing movie details.
    """
    # Initialize TMDb API
    tmdb = TMDb()
    tmdb.api_key = API_KEY

    # Initialize Movie object
    movie_api = Movie()

    # Retrieve movie details from TMDb based on the slug
    tmdb_movie = movie_api.search(slug)
    if tmdb_movie:
        # Assuming the first search result is the desired movie
        tmdb_movie = tmdb_movie[0]  

        movie_details = {
            'id': tmdb_movie.id,
            'title': tmdb_movie.title,
            'slug':slugify(tmdb_movie.title),
            'original_title': tmdb_movie.original_title,
            'genre': get_genres_by_id(tmdb_movie.genre_ids),
            'release_year': tmdb_movie.release_date.split('-')[0] if tmdb_movie.release_date else "",
            'overview': tmdb_movie.overview,
            'poster_path': tmdb_movie.poster_path,
            'rate': tmdb_movie.vote_average,
            'trailer': get_trailer_url_by_id(tmdb_movie.id),
            'views': tmdb_movie.vote_count,
        }
        return movie_details
    else:
        return None
    
# you should never need to get movie info from database since if you have id
# you would also have all other relevant info stored locally
if __name__ == "__main__":
    #test script
    # print(get_movies_by_search("chungus"))
    print(get_movies_by_search("kungfu panda"))