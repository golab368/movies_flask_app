import requests
import os


def call_tmdb_api(endpoint):
    api_key = os.environ.get("api_key")
    base_url = f"https://api.themoviedb.org/3/{endpoint}"
    response = requests.get(f"{base_url}{api_key}")
    response.raise_for_status()
    return response.json()


def get_movies_list(list_type="popular"):
    return call_tmdb_api(f"movie/{list_type}")


def get_poster_url(poster_api_path):
    base_url = "https://image.tmdb.org/t/p/w342/"
    return f"{base_url}/{poster_api_path}"


def get_movies(how_many, list_type):
    data = get_movies_list(list_type)
    return data["results"][:how_many]


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_single_movie_cast(movie_id):
    api_key = os.environ.get("api_key")
    base_url = "https://api.themoviedb.org/3/movie/"
    cast = "/credits"
    ready = requests.get(f"{base_url}{movie_id}{cast}{api_key}")
    return ready.json()["cast"]




