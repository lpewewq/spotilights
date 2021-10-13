from flask import Flask, redirect

from app.lightstrip_controller import LightstripController
from app.spotify_player import SpotifyVisualizer

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

spotify_visualizer = SpotifyVisualizer(app)
lightstrip_controller = LightstripController(app, spotify_visualizer)


@app.route("/")
def index():
    return "<h1><a href=/spotify>Spotify light</a></h1>"


@app.route("/spotify")
def spotify():
    return redirect("/")
