from flask import jsonify, request
from flask_restful import Resource
from imdb import Cinemagoer
from . import db, var


class MovieInformation(Resource):
    def post(self):
        data = request.json
        is_bookmark = db.is_bookmark(imdb_id=int(data["imdb_id"]), user_id=int(data["user_id"]))
        movie = db.get_movie(int(data["imdb_id"]))
        
        all_seasons = []
        for file in movie['episodes']:
            if file['season'] in all_seasons: continue
            all_seasons.append(int(file['season']))
        all_seasons.sort()

        return jsonify({
            "status": True,
            "movie": {"title": movie["title"], "cover": movie["cover"], "rating": movie["rating"]},
            "episodes": movie['episodes'],
            "all_seasons": all_seasons,
            "is_bookmark": is_bookmark,
        })


class ToggleBookmark(Resource):
    def post(self):
        data = request.json
        db.toggle_bookmark(imdb_id=int(data["imdb_id"]), user_id=int(data["user_id"]))
