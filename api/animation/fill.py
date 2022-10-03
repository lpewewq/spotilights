import time

import numpy as np
import tekore as tk
from colour import Color

from ..strip.base import LEDStrip
from . import ColorModel, animator, router
from .base_spotify import BaseSpotifyAnimation


@router.post("/fill")
async def start_fill(color_model: ColorModel):
    animator.start(FillAnimation, color_model.get_color())


class FillAnimation(BaseSpotifyAnimation):
    def __init__(self, strip: LEDStrip, color: Color) -> None:
        super().__init__(strip)
        self.color = color
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
        r, g, b = self.color.get_red(), self.color.get_green(), self.color.get_blue()
        self.strip.fill_color(Color(rgb=(r * beat, g * beat, b * beat)))
        self.strip.show()

    async def on_track_change(
        self,
        currently_playing: tk.model.CurrentlyPlaying,
        audio_analysis: tk.model.AudioAnalysis,
    ) -> None:
        self.bpm = audio_analysis.track["tempo"]
