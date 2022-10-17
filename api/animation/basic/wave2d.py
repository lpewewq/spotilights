import numpy as np

from ...color import Color
from ..base.decorators import on_change
from .bpm import BPMAnimation


class Wave2DAnimation(BPMAnimation):
    def __init__(self, color: Color, fineness: float = 30.0, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color
        self.fineness = fineness

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def change_callback(self, xy: np.ndarray) -> None:
        self.colors = np.full(len(xy), self.color)
        # center
        centered = xy - (xy.max(axis=0) + xy.min(axis=0)) / 2
        # normalize
        normalized = centered / np.max(np.linalg.norm(centered, axis=1))
        # euclid norm
        self.pattern = np.linalg.norm(normalized, axis=1) * self.fineness

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self.colors * self.beat(self.bpm, self.pattern)
