import time
from abc import ABC

import numpy as np
from pydantic import Field, confloat

from ..spotify.models import AudioAnalysis, Beat
from .abstract import AbstractAnimation


class BPM(AbstractAnimation, ABC):
    low: confloat(ge=0, le=1, multiple_of=0.05) = Field(0.0, title="Lower Bound", description="%")
    _bpm: float = 0
    _beat_start = 0
    _beat_duration = 1

    @property
    def needs_spotify(self) -> bool:
        return True

    def beat(self, bpm: float, shift: float = 0.0) -> float:
        bps2pi = 2 * np.pi * bpm / 60
        beat = (np.sin(-time.time() * bps2pi + shift) + 1) / 2
        return self.low + (1 - self.low) * beat

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._beat_start = beat.start
        self._beat_duration = beat.duration
        return super().on_beat(beat, progress)

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self._bpm = analysis.tempo
        return super().on_track_change(analysis)
