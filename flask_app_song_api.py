import configparser

from db import db
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, reqparse

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

songs_fields = {
    '_id': fields.String,
    'artist': fields.String,
    'title': fields.String,
    'difficulty': fields.Float,
    'level': fields.Integer,
    'released': fields.String
}

req_parser = reqparse.RequestParser()
req_parser.add_argument('page_size')

class SongList(Resource):
    @marshal_with(songs_fields)
    def get(self):
        args = req_parser.parse_args()
        return mongodb.getSongs()

api.add_resource(SongList, '/songs')
