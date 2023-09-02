from flask import Flask, render_template, jsonify, request
import os
import flask
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
import json
from json import JSONEncoder
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
    jobs = load_jobs_from_db()
    return render_template(
      'home.html', 
      jobs=jobs,
    )

app.register_blueprint(bp)

app.run()
