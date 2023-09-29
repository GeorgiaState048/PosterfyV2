from flask import Flask, render_template, jsonify, request
import os
import flask
from database import load_job_from_db
import json
from json import JSONEncoder
import base64
import requests
from datetime import datetime, timedelta
app = flask.Flask(__name__)

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.
bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# route for serving React page
@bp.route("/")
def index():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")

@bp.route("/home")
def hello_jovian():
    return render_template(
      'home.html'
    )

def get_spotify_access_token(client_id, client_secret):
    # Spotify API endpoint for obtaining an access token
    token_url = "https://accounts.spotify.com/api/token"

    # Encode the client ID and client secret in base64 format
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    # Set the headers for the token request
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Set the data for the token request
    data = {
        "grant_type": "client_credentials",
    }

    # Make the token request
    response = requests.post(token_url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response to get the access token
        access_token = response.json().get("access_token")
        expires_in = response.json().get("expires_in")

        # Calculate the expiration time of the token
        expiration_time = datetime.now() + timedelta(seconds=expires_in)

        # print(f"Access Token: {access_token}")
        # print(f"Expiration Time: {expiration_time}")

        return access_token
    else:
        # Print an error message if the request was not successful
        # print(f"Error: {response.status_code}, {response.text}")
        return None

# Replace with your own Spotify API client ID and client secret
client_id = "a2b8b16af30f4e1f9bf9b5a86ee8862b"
client_secret = "877d125158854158b128e63d13a7cfdb"

# Get the access token
access_token = get_spotify_access_token(client_id, client_secret)

def test_request(token):
    album_id = "3xybjP7r2VsWzwvDQipdM0"
    user_endpoint = "https://api.spotify.com/v1/albums/" + album_id
    response = requests.get(
        user_endpoint,
        headers={
            "Authorization": "Bearer " + token,
        },
    )
    response_json = response.json()
    print(response_json["images"])

test_request(access_token)

# app.register_blueprint(bp)

# app.run()
