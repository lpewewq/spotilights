from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from ..spotify.models import Beat
from .abstract import AbstractAnimation
from .utils import beat
from .utils.decorators import on_change


class Wave2D(AbstractAnimation):
    """2D Wave animation."""

    name: Literal["Wave2D"]
    color: Color = Field(Color(r=255), type="color", title="Fill Color")
    low: confloat(ge=0, le=1, multiple_of=0.05) = Field(0.0, title="Lower Bound", description="%")
    fineness: confloat(ge=0, le=100, multiple_of=1) = Field(30.0, title="Fineness", description=" ")
    _bpm = 0

    def change_elements_callback(self, xy: np.ndarray) -> None:
        self.colors = np.full(len(xy), self.color)
        self._pattern = np.linalg.norm(xy, axis=1) * self.fineness

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self.colors * beat(self._bpm, self._pattern, self.low)

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._bpm = 60.0 / beat.duration
        return super().on_beat(beat, progress)
