import time

import numpy as np

from ..color import Color, IntColorModel
from ..spotify import spotify_animator
from . import router
from .base import BaseAnimation


@router.post("/fill")
async def start_fill(color_model: IntColorModel):
    await spotify_animator.start(FillAnimation, color_model.get_color())


class FillAnimation(BaseAnimation):
    def __init__(self, color: Color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color
        self.low = 0.5
        self.high = 1.0
        self.beat = lambda: self.high

    def _beatsin(self, bps2pi: float, low: float, diff: float) -> float:
        return low + diff * (np.sin(time.time() * bps2pi) + 1) / 2

    async def set_beat(self):
        audio_analysis = await self.shared_data.get_audio_analysis()
        if audio_analysis:
            bpm = audio_analysis.track["tempo"]
            bps2pi = 2 * np.pi * bpm / 60
            self.beat = lambda: self._beatsin(bps2pi, self.low, self.high - self.low)

    async def on_pause(self) -> None:
        self.beat = lambda: self.high

    async def on_resume(self) -> None:
        await self.set_beat()

    async def on_track_change(self) -> None:
        await self.set_beat()

    async def on_loop(self) -> None:
        self.strip.fill_color(self.color.scale(self.beat()))
        self.strip.show()
