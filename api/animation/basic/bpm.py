import time
from abc import ABC

import numpy as np
from pydantic import confloat

from ...spotify.models import AudioAnalysis
from ..base import Animation


class BPM(Animation, ABC):
    def __init__(self, config: "BPM.Config") -> None:
        super().__init__(config)
        self.config: BPM.Config
        self.bpm: float = 0

    class Config(Animation.Config):
        low: confloat(ge=0, le=1, multiple_of=0.05) = 0.0
        high: confloat(ge=0, le=1, multiple_of=0.05) = 1.0

        @property
        def needs_spotify(self) -> bool:
            return True

    def beat(self, bpm: float, shift: float = 0.0) -> float:
        bps2pi = 2 * np.pi * bpm / 60
        beat = (np.sin(-time.time() * bps2pi + shift) + 1) / 2
        return self.config.low + (self.config.high - self.config.low) * beat

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self.bpm = analysis.tempo
