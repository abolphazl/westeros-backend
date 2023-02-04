from flask import jsonify, request
from flask_restful import Resource
from dotenv import load_dotenv
from threading import Thread
from imdb import Cinemagoer
from pyrogram import Client
from . import db, var
import requests
import os


class MovieInformation(Resource):
    def post(self):
        try:
            data = request.json
            is_bookmark = db.is_bookmark(imdb_id=int(data["imdb_id"]), user_id=int(data["user_id"]))
            movie = db.get_movie(int(data["imdb_id"]))
        except:
            return jsonify({"status": False})
        
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
        try:
            data = request.json
            db.toggle_bookmark(imdb_id=int(data["imdb_id"]), user_id=int(data["user_id"]))
        except:
            return


class SendFile(Resource):
    def post(self):
        try:
            data = request.json
            load_dotenv()

            caption = "some caption!"

            url  = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/copyMessage?chat_id={data['user_id']}&from_chat_id={-1001693241710}&message_id={data['mid']}&caption={caption}"
            requests.get(url)
        except Exception as e:
            print(e)
            return