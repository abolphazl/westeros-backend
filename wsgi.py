from flask_restful import Resource, Api
from flask import Flask, jsonify
from flask_cors import CORS
from plugins import admin
from plugins import db

# creating flask app and api object
app = Flask(__name__)
CORS(app)
api = Api(app)
db.setup_tables()

# handlers
api.add_resource(admin.InsertMovie, '/insert-movie/<int:imdb_id>')
api.add_resource(admin.Search, '/search/<string:query>')
api.add_resource(admin.InsertEpisode, '/insert-episode')
api.add_resource(admin.Movie, '/movie/<int:imdb_id>')

# driver function
if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')