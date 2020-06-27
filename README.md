# song-api
A REST API exercise using Python and Flask.

## Environment setup

For this project you require a free local MongoDB database server.
You can download it from https://www.mongodb.com/.

It is highly recommended to run everything in an up-to-date virtualenv.
The project requires python3 to run properly. The environment can be set up
using either:

`python3 -m venv venv`
`. venv/bin/activate`

OR on Windows:

`py -3 -m venv venv`
`venv\Scripts\activate`

In order to run the project, requirements need to be installed. This can be
done by typing:

`pip install -r requirements.txt`

## Running the application

It is recommended to run the application by the flask command. In order to
do that, you need to export the FLASK_APP environment variable:

`export FLASK_APP=flask_app_song_api.py`

OR on Windows:

`set FLASK_APP=flask_app_song_api.py`

(Optional) If you wish to run the application in development mode, for example to use hot reload,
export the FLASK_ENV environment variable as:

`export FLASK_ENV=development`

OR on Windows:

`set FLASK_ENV=development`

Now you may run the application using:

`flask run`
