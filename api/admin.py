from flask import jsonify, request, send_file
from flask_restful import Resource
from imdb import Cinemagoer
from . import db, var

USERNAME = "admin"
PASSWORD = "12345678"


class InsertMovie(Resource):
    def get(self, imdb_id):
        try:            
            if db.movie_exists(imdb_id):
                return jsonify({"message": "Movie exists."})

            ia = Cinemagoer()
            movie = ia.get_movie(str(imdb_id))
            db.insert_movie({
                "imdb_id": imdb_id,
                "title": movie['title'],
                "rating": movie['rating'],
                "cover": movie['full-size cover url']
            })

            return jsonify({"message": f"movie inserted successfully"})
        except Exception as e:
            print(e)
            return jsonify({"message": f"imdb id is wrong!"})


class Search(Resource):
    def get(self, query):
        if query == '$$$':
            data = db.recent_movies()
            return jsonify({"result": data[:20]})
        try:
            data = db.like(query)
            return jsonify({"result": data[:20]})
        except:
            return jsonify({"result": []})


class InsertEpisode(Resource):
    def post(self):
        data = request.json
        if db.episode_exists(data['mid']): return jsonify({"status": False, "message": "MID is exists"})
        db.insert_episode(data)
        return jsonify({"status": True, "message": "Episode inserted successfully"})


class Movie(Resource):
    def get(self, imdb_id):
        if db.movie_exists(imdb_id) == False: return jsonify({"status": False, "message": "Movie not found"})
        data = db.get_movie(imdb_id)
        data['status'] = True
        return jsonify(data)


class DeleteEpisode(Resource):
    def get(self, mid):
        db.delete_episode(mid)
        return jsonify({"status": True, "message": "deleted successfully"})


class CheckUser(Resource):
    def post(self):
        try:
            data = request.json
            if data['password'] == PASSWORD and data['username'] == USERNAME:
                return jsonify({"status": True})
            else:
                return jsonify({"status": False})
        except:
            return


class Backup(Resource):
    def get(self):
        path = var.db_path
        return send_file(path, as_attachment=True)
        
