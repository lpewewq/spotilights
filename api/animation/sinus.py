from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from .bpm import BPM
from .utils.decorators import on_change


class Sinus(BPM):
    """Gaussian bell sinus slide on beat."""

    name: Literal["Sinus"]
    color: Color = Field(Color(r=255), type="color", title="Fill Color")

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        bell = lambda i: (0.1 + 0.9 / np.sqrt(1 + (i - n) ** 2))
        colors = np.full(2 * n + 1, self.color)
        self.pattern = colors * bell(np.arange(2 * n + 1))

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat = self.beat(self._bpm / 2)
        offset = round(beat * n)
        return self.pattern[offset : offset + n]
