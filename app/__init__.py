from flask import Flask, redirect

from app.lightstrip_controller import LightstripController
from app.visualizer.spotify.philipp import PhilippsSpotifyVisualizer
from app.visualizer.spotify.philipp_audio import PhilippsAudioSpotifyVisualizer
from app.visualizer.ambient.pride import PrideVisualizer

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

lightstrip_controller = LightstripController(app)
lightstrip_controller.start_visualization(PrideVisualizer(app))


@app.route("/")
def index():
    return """<h1><a href=/philipp>philipp</a></h1> 
              <h1><a href=/philipp_audio>philipp_audio</a></h1>
              <h1><a href=/pride>pride</a></h1>"""


@app.route("/philipp")
def philipp():
    lightstrip_controller.start_visualization(PhilippsSpotifyVisualizer(app))
    return redirect("/")


@app.route("/philipp_audio")
def philipp_audio():
    lightstrip_controller.start_visualization(PhilippsAudioSpotifyVisualizer(app))
    return redirect("/")


@app.route("/pride")
def pride():
    lightstrip_controller.start_visualization(PrideVisualizer(app))
    return redirect("/")
