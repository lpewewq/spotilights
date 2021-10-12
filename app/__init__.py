from flask import Flask, redirect

from app.ambient_visualizer import AmbientVisualizer
from app.lightstrip_state import LightstripState
from app.spotify_player import SpotifyVisualizer
from app.visualizer import Visualizer

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")


visualizer = Visualizer(LightstripState(app))
spotify_visualizer = SpotifyVisualizer(app, visualizer.leds)
visualizer.start(spotify_visualizer)


@app.route("/")
def index():
    return (
        "<h1><a href=/spotify>Spotify light</a></h1>"
        "<h1><a href=/ambient>Rainbow</a></h1>"
    )


@app.route("/spotify")
def spotify():
    visualizer.start(spotify_visualizer)
    return redirect("/")


@app.route("/ambient")
def ambient():
    visualizer.end()
    visualizer.start(AmbientVisualizer())
    return redirect("/")
