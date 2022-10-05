import time

import numpy as np

from ..color import Color, IntColorModel
from ..spotify import spotify_animator
from ..spotify.shared_data import SharedData
from . import router
from .base import Animation


@router.post("/fill")
async def start_fill(color_model: IntColorModel):
    animation = FillAnimation(color_model.get_color())
    await spotify_animator.start(animation)


class FillAnimation(Animation):
    def __init__(self, color: Color, shift: float = 0.0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color
        self.shift = shift
        self.low = 0.5
        self.high = 1.0
        self.beat = lambda: self.high

    def _beatsin(self, bps2pi: float, low: float, diff: float, shift: float) -> float:
        return low + diff * (np.sin(time.time() * bps2pi + shift) + 1) / 2

    async def set_beat(self, shared_data: SharedData):
        audio_analysis = await shared_data.get_audio_analysis()
        if audio_analysis:
            bpm = audio_analysis.track["tempo"]
            bps2pi = 2 * np.pi * bpm / 60
            self.beat = lambda: self._beatsin(bps2pi, self.low, self.high - self.low, self.shift * 2 * np.pi)

    async def on_pause(self, shared_data: SharedData) -> None:
        self.beat = lambda: self.high

    async def on_resume(self, shared_data: SharedData) -> None:
        await self.set_beat(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        await self.set_beat(shared_data)

    async def on_loop(self) -> None:
        self.strip.fill_color(self.color * self.beat())

    @property
    def depends_on_spotify(self) -> bool:
        return True
