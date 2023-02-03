from flask_restful import Resource, Api
from plugins import admin, movies
from flask import Flask, jsonify
from flask_cors import CORS

# creating flask app and api object
app = Flask(__name__)
CORS(app)
api = Api(app)

# handlers
api.add_resource(admin.InsertMovie, '/insert-movie/<int:imdb_id>')
api.add_resource(admin.Search, '/search/<string:query>')
api.add_resource(admin.InsertEpisode, '/insert-episode')
api.add_resource(admin.Movie, '/movie/<int:imdb_id>')
api.add_resource(admin.DeleteEpisode, "/delete-episode/<int:mid>")
api.add_resource(admin.CheckUser, '/check-user')
api.add_resource(admin.Backup, '/backup')
api.add_resource(movies.MovieInformation, '/movies')
api.add_resource(movies.ToggleBookmark, '/toggle-bookmark')

# driver function
if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')