from flask import Flask, render_template, jsonify, request
import os
import flask
from PIL import Image
import io
import json
from json import JSONEncoder
import urllib.request
import base64
import requests
from datetime import datetime, timedelta
# from database import load_job_from_db


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

    print("about to make request")
    # Make the token request
    response = requests.post(token_url, headers=headers, data=data)
    print("made request")
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

def test_request(token):
    user_endpoint = "https://api.spotify.com/v1/browse/new-releases?country=US&locale=en-US%2Cen%3Bq%3D0.9&offset=0&limit=20"
    response = requests.get(
        user_endpoint,
        headers={
            "Authorization": "Bearer " + token,
        },
        timeout=10
    )
    response_json = response.json()
    new_release = response_json["albums"]["items"]

@bp.route("/poster")
def get_album_covers():
    """Get new album releases and display them on poster page"""
    token = get_spotify_access_token(client_id, client_secret)
    user_endpoint = "https://api.spotify.com/v1/browse/new-releases?country=US&locale=en-US%2Cen%3Bq%3D0.9&offset=0&limit=20"
    response = requests.get(
        user_endpoint,
        headers={
            "Authorization": "Bearer " + token,
        },
        timeout=10
    )
    response_json = response.json()
    new_release = response_json["albums"]["items"]
    for i in new_release:
        print(i["images"][0]["url"])
    return render_template(
        'poster.html',
        new_release=new_release,
        len = len(new_release)
    )

def create_combined_image():
    # Open the images
    image1 = Image.open(requests.get("https://i.scdn.co/image/ab67616d0000b273c1156c6f6dedd4b9bdf89428", stream=True, timeout=10).raw)
    image2 = Image.open(requests.get("https://i.scdn.co/image/ab67616d0000b273f6549a3f99e338b94d7ddc08", stream=True, timeout=10).raw)

    # Ensure both images have the same size
    image2 = image2.resize(image1.size)

    # Create a new image with the same size as the input images
    new_image = Image.new("RGBA", image1.size)

    # Paste the first image onto the new image
    new_image.paste(image1, (0, 0))

    # Paste the second image with transparency
    new_image.paste(image2, (100, 100), mask=image2)

    # Save the result to a BytesIO object
    image_io = io.BytesIO()
    new_image.save(image_io, format="PNG")
    image_io.seek(0)

    return image_io

@bp.route("/testposter")
def test_poster():
    combined_images = create_combined_image()
    return flask.render_template(
        "testposter.html",
        image_data=combined_images.read()
    )

# test_request(access_token)

app.register_blueprint(bp)

app.run()
