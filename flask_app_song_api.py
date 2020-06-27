import configparser

from db import db
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, reqparse
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

class SongList(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('page_size')

    @marshal_with(song_fields)
    def get(self):
        args = self.req_parser.parse_args()
        return mongodb.getSongs({}, None)

class SongsByDifficulty(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('level')

    def get(self):
        args = self.req_parser.parse_args()
        query = {}
        if args['level']:
            query['level'] = int(args['level'])
        songs = mongodb.getSongs(query, {'difficulty': 1})
        song_difficulties = [song['difficulty'] for song in songs]
        if not song_difficulties:
            return 0
        return mean(song_difficulties)

api.add_resource(SongList, '/songs')
api.add_resource(SongsByDifficulty, '/songs/avg/difficulty')
