from tinydb import TinyDB, where, Query
import os, time, re
from . import var


# settings
User = Query()
tables  = {
    "members": ('user_id', 'join_in', 'status' ),
    "movies" : ('imdb_id', 'title'  , 'rating' , 'cover'),
    "files"  : ('imdb_id', 'season' , 'episode', 'quality', 'mid'),
    "bookmarks": ("imdb_id", "user_id"),
}


# movie exists
def movie_exists(imdb_id):
    if TinyDB(var.db_path).table("movies").contains(where("imdb_id") == int(imdb_id)):
        return True
    return False


# get movie
def get_movie(imdb_id):
    movie = TinyDB(var.db_path).table("movies").get(where("imdb_id") == imdb_id)
    episodes = TinyDB(var.db_path).table("files").search(where("imdb_id") == imdb_id)
    movie['episodes'] = episodes
    return movie


# insert movie
def insert_movie(data):
    TinyDB(var.db_path).table("movies").upsert(data, where("imdb_id") == data["imdb_id"])


# insert episode
def insert_episode(data):
    TinyDB(var.db_path).table("files").upsert({
        "imdb_id": int(data["imdb_id"]),
        "season": int(data["season"]),
        "episode": int(data["episode"]),
        "quality": int(data["quality"]),
        "mid": int(data["mid"]),
    }, where("mid") == int(data["mid"]))


# episode exists
def episode_exists(mid):
    if TinyDB(var.db_path).table("files").contains(where("mid") == int(mid)):
        return True
    return False 


# delete episode
def delete_episode(mid):
    TinyDB(var.db_path).table("files").remove(where("mid") == int(mid))


def recent_movies():
    movies = TinyDB(var.db_path).table("movies").all()
    return movies[:20]


def like(query):
    results = TinyDB(var.db_path).table("movies").search(User.title.matches(query, flags=re.IGNORECASE))
    return results[:10]


def is_bookmark(imdb_id, user_id):
    if TinyDB(var.db_path).table("bookmarks").contains((where("imdb_id") == imdb_id) & (where("user_id") == user_id)):
        return True
    return False


def toggle_bookmark(imdb_id, user_id):
    bookmarks = TinyDB(var.db_path).table("bookmarks")
    if bookmarks.contains((where("imdb_id") == imdb_id) & (where("user_id") == user_id)):
        bookmarks.remove((where("imdb_id") == imdb_id) & (where("user_id") == user_id))
    else:
        bookmarks.insert({"imdb_id": imdb_id, "user_id": user_id})
