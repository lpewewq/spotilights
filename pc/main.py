from flask import Flask, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

from LightstripState import LightstripState
from Visualizer import Visualizer
from MusicPlaybackState import MusicPlaybackState
from MusicVisualizer import MusicVisualizer
from AmbientVisualizer import AmbientVisualizer

sp                = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state", redirect_uri='http://127.0.0.1:5001'))
leds              = LightstripState("/dev/ttyUSB0", 180)
currVisualization = Visualizer(leds, AmbientVisualizer(leds).callback)
currVisualization.startVisualization()

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1><a href=/spotify>Spotify light</a></h1>" \
           "<h1><a href=/ambient>Ambient light</a></h1>"

@app.route('/spotify')
def spotify():
    global leds
    global currVisualization

    track = sp.current_playback()
    if track is None:
        return "No track playing right now"
    analysis = sp.audio_analysis(track["item"]["id"])
    start = time.time()
    track = sp.current_playback()
    time_offset = track["progress_ms"] / 1000 + (time.time() - start) / 2

    currVisualization.endVisualization()
    currVisualization = Visualizer(leds, MusicPlaybackState(analysis, time_offset, MusicVisualizer(leds)).callback)
    currVisualization.startVisualization()
    return redirect("/")

@app.route('/ambient')
def ambient():
    global currVisualization
    currVisualization.endVisualization()
    currVisualization = Visualizer(leds, AmbientVisualizer(leds).callback)
    currVisualization.startVisualization()
    return redirect("/")