import numpy as np

from ...color import Color
from .bpm import BPM


class Fill(BPM):
    def __init__(self, color: Color, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        color = self.color * self.beat(self.bpm)
        return np.full(len(xy), color)
