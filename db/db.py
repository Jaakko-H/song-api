import json
import pymongo

class MongoDB(object):
    __db = None
    collection_songs = 'songs'
    collection_song_ratings = 'song_ratings'

    def __init__(self, db_config):
        mongo_client = pymongo.MongoClient(db_config['mongodb_url'])
        self.__db = mongo_client[db_config['db_name']]
        self.clear_songs_collection()
        self.import_songs_data_from_json()

    def get_songs(self, query, fields_to_return):
        return list(self.__db[self.collection_songs].find(query, fields_to_return))

    def clear_songs_collection(self):
        self.__db[self.collection_songs].delete_many({})

    def import_songs_data_from_json(self):
        with open('songs.json') as songs_file:
            for line in songs_file:
                self.__db[self.collection_songs].insert_one(json.loads(line))
