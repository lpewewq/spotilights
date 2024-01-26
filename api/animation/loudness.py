from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..spotify.models import AudioAnalysis
from .abstract import SingleSub


class ScaleLoudness(SingleSub):
    """Container scaling an animation by song loudness."""

    class Config:
        title = "Scale Loudness"

    name: Literal["ScaleLoudness"]
    sensitivity: confloat(ge=0, le=10, multiple_of=0.1) = Field(
        6, title="Sensitivity", description=" "
    )
    _scaling = 0
    _loudness_interpolation = None

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self._loudness_interpolation = analysis.loudness_interpolation
        return super().on_track_change(analysis)

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        try:
            self._scaling = self._loudness_interpolation(progress)
        except (TypeError, ValueError):
            self._scaling *= 0.95  # fade out
        return super().render(progress, xy) * (self._scaling**self.sensitivity)
