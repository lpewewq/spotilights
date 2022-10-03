import time

import numpy as np
import tekore as tk
from rpi_ws281x import Color

from .base_spotify import BaseSpotifyAnimation


class FillAnimation(BaseSpotifyAnimation):
    def __init__(self, strip: "LEDStrip", color_model: "ColorModel") -> None:
        super().__init__(strip)
        self.color_model = color_model
        self.bpm = None

    def beatsin88(self, bpm, lowest, highest) -> int:
        beat = time.time() * np.pi * bpm / 7680
        beatsin = (np.sin(beat) + 1) / 2
        rangewidth = highest - lowest
        return int(lowest + rangewidth * beatsin)

    async def loop(self) -> None:
        if self.bpm:
            beat = self.beatsin88(self.bpm * 256, 128, 255) / 255
        else:
            beat = 1.0
        red = int(self.color_model.red * beat)
        green = int(self.color_model.green * beat)
        blue = int(self.color_model.blue * beat)
        self.strip.fillColor(Color(red, green, blue))
        self.strip.show()

    async def on_track_change(
        self,
        currently_playing: tk.model.CurrentlyPlaying,
        audio_analysis: tk.model.AudioAnalysis,
    ) -> None:
        self.bpm = audio_analysis.track["tempo"]
        print("Changed track:", currently_playing.item.name, self.bpm)

    async def on_beat(self, beat: tk.model.TimeInterval) -> None:
        print("Beat!", beat.start, beat.duration)

    async def on_section(self, section: tk.model.TimeInterval) -> None:
        print("Section!", section.start, section.duration)
