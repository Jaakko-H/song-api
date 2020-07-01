import os
import tempfile
import pytest

from flaskr import flask_app_song_api

@pytest.fixture
def client():
    flask_app_song_api.app.config['TESTING'] = True

    with flask_app_song_api.app.test_client() as client:
        yield client

def test_get_songs(client):
    response = client.get('/songs')
    assert 11 == len(response.get_json())

def test_get_avg_difficulty(client):
    response = client.get('/songs/avg/difficulty?level=3')
    assert 2 == response.get_json()

def test_get_songs_search(client):
    response = client.get('/songs/search?message=You')
    assert 10 == len(response.get_json())
