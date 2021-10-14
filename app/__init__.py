from flask import Flask, redirect

from app.lightstrip_controller import LightstripController
from app.visualizer.spotify_visualizer.philipps_spotify_visualizer import (
    PhilippsSpotifyVisualizer,
)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

spotify_visualizer = PhilippsSpotifyVisualizer(app)
lightstrip_controller = LightstripController(app)
lightstrip_controller.start_visualization(spotify_visualizer)


@app.route("/")
def index():
    return "<h1><a href=/spotify>Spotify light</a></h1>"


@app.route("/spotify")
def spotify():
    lightstrip_controller.start_visualization(spotify_visualizer)
    return redirect("/")
