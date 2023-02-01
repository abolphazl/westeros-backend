import sqlite3, os, time
from . import var


# settings
tables  = {
    "members": ('user_id', 'join_in', 'status' ),
    "movies" : ('imdb_id', 'title'  , 'rating' , 'cover'),
    "files"  : ('imdb_id', 'season' , 'episode', 'quality', 'mid')
}

# connect to sqlite
con = sqlite3.connect(var.db_path, check_same_thread=False)
cur = con.cursor()

# check table is exists
def table_exists(name: str) -> bool:
    res = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{name}'")
    return res.fetchone() != None

# create table
def create_table(table: str, items: tuple):
    cur.execute(f"CREATE TABLE {table}{items}")

# setup tables
def setup_tables():
    global tables
    for table in tables:
        if table_exists(table): continue
        create_table(table=table, items=tables[table])

# movie exists
def movie_exists(imdb_id):
    res = cur.execute(f"SELECT imdb_id FROM movies WHERE imdb_id={imdb_id}")
    return res.fetchone() != None

# get movie
def get_movie(imdb_id):
    movie = cur.execute(f"SELECT * FROM movies WHERE imdb_id={imdb_id}").fetchone()
    episodes = cur.execute(f"SELECT * FROM files WHERE imdb_id={imdb_id} ORDER BY season").fetchall()
    data = {"imdb_id": movie[0], "title": movie[1], "rating": movie[2], "cover": movie[3]}
    data['episodes'] = [ 
        {"season": e[1], "episode": e[2], "quality": e[3], "mid": e[4]}
        for e in episodes
    ]
    return data

# insert movie
def insert_movie(data):
    cur.execute(f"INSERT INTO movies VALUES ({data['imdb_id']}, '{data['title']}', {data['rating']}, '{data['cover']}')")
    con.commit()

# insert episode
def insert_episode(data):
    cur.execute(f"INSERT INTO files VALUES ({data['imdb_id']}, {data['season']}, {data['episode']}, {data['quality']}, {data['mid']})")
    con.commit()

# episode exists
def episode_exists(mid):
    res = cur.execute(f"SELECT imdb_id FROM files WHERE mid={mid}")
    return res.fetchone() != None

# delete episode
def delete_episode(mid):
    cur.execute(f"DELETE FROM files WHERE mid={mid}")
    con.commit()

def recent_movies():
    res = cur.execute(f"SELECT * FROM movies").fetchall()
    if res == None or len(res) == 0: return []
    return [
        {"imdb_id": movie[0], "title": movie[1], "rating": movie[2], "cover": movie[3]}
        for movie in res
    ]

def like(query):
    res = cur.execute(f"SELECT * FROM movies WHERE title LIKE '%{query}%'").fetchall()
    return [
        {"imdb_id": movie[0], "title": movie[1], "rating": movie[2], "cover": movie[3]}
        for movie in res
    ]











# get all users
# def get_all_users():
#     all_users = cur.execute("SELECT * FROM members").fetchall()
#     return [
#         {"user_id": user[0], "lang": user[1], "join_in": user[2], "status": user[3]}
#         for user in all_users
#     ]