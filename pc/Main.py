from flask import Flask, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

from LightstripState import LightstripState
from Visualizer import Visualizer
from MusicPlaybackState import MusicPlaybackState
from MusicVisualizer import MusicVisualizer
from AmbientVisualizer import AmbientVisualizer
from SpotifyPlayer import SpotifyPlayer

visualizer        = Visualizer(LightstripState("/dev/ttyUSB0", 180))
player            = SpotifyPlayer(
                        spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state", redirect_uri='http://127.0.0.1:5001')),
                        visualizer)
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1><a href=/spotify>Spotify light</a></h1>" \
           "<h1><a href=/ambient>Rainbow</a></h1>"

@app.route('/spotify')
def spotify():
    player.startCurrentSongVisualization()
    return redirect("/")

@app.route('/ambient')
def ambient():
    visualizer.endVisualization()
    visualizer.startVisualization(AmbientVisualizer(visualizer.leds).callback)
    return redirect("/")