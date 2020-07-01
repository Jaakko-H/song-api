import os
import tempfile
import pytest

from flaskr import flask_app_song_api

@pytest.fixture
def client():
    flask_app_song_api.app.config['TESTING'] = True

    with flask_app_song_api.app.test_client() as client:
        with flask_app_song_api.app.app_context():
            flask_app_song_api.mongodb.clear_song_ratings_collection()
        yield client

def test_get_songs(client):
    response = client.get('/songs').get_json()
    assert 11 == len(response)

def test_get_avg_difficulty(client):
    response = client.get('/songs/avg/difficulty?level=3').get_json()
    assert 2 == response

def test_get_songs_search(client):
    response = client.get('/songs/search?message=You').get_json()
    assert 10 == len(response)

def test_post_song_rating(client):
    song_id = client.get('/songs?page_size=1').get_json()[0]['_id']
    response = client.post('/songs/rating?song_id={}&rating=5'.format(song_id))
    assert '200 OK' == response.status
    assert response.get_json()

def test_get_song_avg_rating(client):
    song_id = client.get('/songs?page_size=1').get_json()[0]['_id']
    client.post('/songs/rating?song_id={}&rating=4'.format(song_id))
    client.post('/songs/rating?song_id={}&rating=2'.format(song_id))
    response = client.get('/songs/avg/rating/' + song_id).get_json()
    assert 3 == response['average']
    assert 2 == response['lowest']
    assert 4 == response['highest']
