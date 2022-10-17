import numpy as np

from ...color import Color
from ..base.decorators import on_change
from .bpm import BPMAnimation


class SinusAnimation(BPMAnimation):
    def __init__(self, color: Color, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        bell = lambda i: (0.1 + 0.9 / np.sqrt(1 + (i - n) ** 2))
        colors = np.full(2 * n + 1, self.color)
        self.pattern = colors * bell(np.arange(2 * n + 1))

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat = self.beat(self.bpm / 2)
        offset = round(beat * n)
        return self.pattern[offset: offset + n]
