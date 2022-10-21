import time
from abc import ABC

import numpy as np

from ...spotify.shared_data import SharedData
from ..base import Animation


class BPM(Animation, ABC):
    def __init__(self, low: float = 0.0, high: float = 1.0) -> None:
        super().__init__()
        self.low = low
        self.high = high
        self.bpm: float = 0

    def beat(self, bpm: float, shift: float = 0.0) -> float:
        bps2pi = 2 * np.pi * bpm / 60
        diff = self.high - self.low
        beat = (np.sin(-time.time() * bps2pi + shift) + 1) / 2
        return self.low + diff * beat

    async def on_pause(self, shared_data: SharedData) -> None:
        self.bpm = 0

    async def on_resume(self, shared_data: SharedData) -> None:
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    async def on_track_change(self, shared_data: SharedData) -> None:
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    @property
    def depends_on_spotify(self) -> bool:
        return True
