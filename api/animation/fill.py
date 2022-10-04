import time

import numpy as np
import tekore as tk
from functools import partial
from ..color import Color, IntColorModel
from ..strip.base import LEDStrip
from . import animator, router
from .base_spotify import BaseSpotifyAnimation


@router.post("/fill")
async def start_fill(color_model: IntColorModel):
    animator.start(FillAnimation, color_model.get_color())


class FillAnimation(BaseSpotifyAnimation):
    def __init__(self, strip: LEDStrip, color: Color) -> None:
        super().__init__(strip)
        self.color = color
        self.low = 0.5
        self.high = 1.0
        self.beat = lambda: self.high

    def _beatsin(self, bps2pi, low, diff):
        return low + diff * (np.sin(time.time() * bps2pi) + 1) / 2

    async def set_beat(self):
        audio_analysis = await self.get_audio_analysis()
        if audio_analysis:
            bpm = audio_analysis.track["tempo"]
            bps2pi = 2 * np.pi * bpm / 60
            self.beat = lambda: self._beatsin(bps2pi, self.low, self.high - self.low)

    async def on_pause(self) -> None:
        await super().on_pause()
        self.beat = lambda: self.high

    async def on_resume(self) -> None:
        await super().on_resume()
        await self.set_beat()

    async def on_track_change(self) -> None:
        await super().on_track_change()
        await self.set_beat()

    async def on_section(self, section: tk.model.TimeInterval) -> None:
        return await super().on_section(section)

    async def on_beat(self, beat: tk.model.TimeInterval) -> None:
        return await super().on_beat(beat)

    async def loop(self) -> None:
        await super().loop()
        self.strip.fill_color(self.color.scale(self.beat()))
        self.strip.show()
