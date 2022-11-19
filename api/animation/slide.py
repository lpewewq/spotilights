from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from .bpm import BPM
from .utils.decorators import on_change
from .utils.ease import EaseFunction, get_ease_function


class Slide(BPM):
    """Slide pattern."""

    name: Literal["Slide"]
    color: Color = Field(Color(r=255), type="color", title="Fill Color")
    ease_function: EaseFunction = "Quint Out"

    @property
    def needs_spotify(self) -> bool:
        return True

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        colors = np.full(2 * n, Color(0, 0, 0))
        colors[(3 * n) // 4 : (3 * n) // 4 + n // 2] = np.full(n // 2, self.color)
        self.pattern = colors

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat_progress = min(1, (progress - self._beat_start) / self._beat_duration)
        beat_progress = get_ease_function(self.ease_function)(beat_progress)
        offset = (3 * n) // 4 - round(beat_progress * (n // 2))
        return self.pattern[offset : offset + n]
