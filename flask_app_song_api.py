import configparser

from db import db
from flask import Flask

app = Flask(__name__)
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
    print('Could not read configuration from file config.cfg: ' + str(e))
    print('Using default configuration instead.')

print('config: ' + str(db_config))
mongodb = db.MongoDB(db_config)

@app.route('/songs')
def getSongs():
    return 'Hello, World!'
