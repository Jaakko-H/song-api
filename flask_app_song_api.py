import configparser
import re

from bson.objectid import ObjectId
from db import db
from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from operator import attrgetter
from statistics import mean

app = Flask(__name__)
api = Api(app)
db_config = {
    'mongodb_url': 'mongodb://localhost:27017/',
    'db_name': 'songdb'
}

try:
    config_parser = configparser.ConfigParser()
    config_parser.read('config.cfg')
    db_config['mongodb_url'] = config_parser['db'].get('mongodb_url')
    db_config['db_name'] = config_parser['db'].get('db_name')
except Exception as e:
    print('Could not read configuration values from file config.cfg: ' + str(e))
    print('Using default configuration instead.')

mongodb = db.MongoDB(db_config)

song_fields = {
    '_id': fields.String,
    'artist': fields.String,
    'title': fields.String,
    'difficulty': fields.Float,
    'level': fields.Integer,
    'released': fields.String
}

def abort_if_rating_not_in_range(rating):
    if not rating >= 1 or not rating <= 5:
        abort(400, message='Rating {} not in range of 1-5.'.format(rating))

def abort_if_song_doesnt_exist(song_id):
    if not mongodb.get_songs({'_id': ObjectId(song_id)}):
        abort(404, message="Song with id {} doesn't exist".format(song_id))

class SongList(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('page_number', type=int, help='Requires page_size parameter')
    req_parser.add_argument('page_size', type=int)

    @marshal_with(song_fields)
    def get(self):
        args = self.req_parser.parse_args()
        return mongodb.get_songs({}, page_number=args['page_number'], page_size=args['page_size'])

class SongAvgDifficulty(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('level', type=int)

    def get(self):
        args = self.req_parser.parse_args()
        query = {}
        if args['level']:
            query['level'] = int(args['level'])
        songs = mongodb.get_songs(query, {'difficulty': 1})
        if not songs:
            return 0
        song_difficulties = [song['difficulty'] for song in songs]
        return mean(song_difficulties)

class SongSearch(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('message', required=True)

    @marshal_with(song_fields)
    def get(self):
        args = self.req_parser.parse_args()
        searchRegex = re.compile('.*' + args['message'] + '.*', re.IGNORECASE)
        return mongodb.get_songs(
                {'$or': [ {'artist': searchRegex}, {'title': searchRegex} ] })

class SongRating(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('song_id', required=True)
    req_parser.add_argument('rating', required=True, type=int, help='Rating must be a number between 1 and 5.')

    def post(self):
        args = self.req_parser.parse_args()
        abort_if_rating_not_in_range(args['rating'])
        return mongodb.insert_song_rating(
                {'song_id': args['song_id'], 'rating': args['rating']})

class SongAvgRating(Resource):
    def get(self, song_id):
        abort_if_song_doesnt_exist(song_id)
        song_ratings = mongodb.get_song_ratings({'song_id': song_id})
        if not song_ratings:
            return {
                'song_id': song_id,
                'average': 0,
                'lowest': 0,
                'highest': 0
            }
        return self.__get_average_lowest_highest_rating(song_id, song_ratings)

    def __get_average_lowest_highest_rating(self, song_id, song_ratings):
        ratings = [song_rating['rating'] for song_rating in song_ratings]
        return {
            'song_id': song_id,
            'average': mean(ratings),
            'lowest': min(ratings),
            'highest': max(ratings)
        }

api.add_resource(SongList, '/songs')
api.add_resource(SongAvgDifficulty, '/songs/avg/difficulty')
api.add_resource(SongSearch, '/songs/search')
api.add_resource(SongRating, '/songs/rating')
api.add_resource(SongAvgRating, '/songs/avg/rating/<song_id>')
