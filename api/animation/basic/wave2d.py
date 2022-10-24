import numpy as np
from pydantic import confloat

from ...color import Color
from ..base.decorators import on_change
from .bpm import BPM


class Wave2D(BPM):
    def __init__(self, config: "Wave2D.Config") -> None:
        super().__init__(config)
        self.config: Wave2D.Config

    class Config(BPM.Config):
        color: Color = Color(r=255)
        fineness: confloat(le=0, ge=100) = 30.0

    def change_callback(self, xy: np.ndarray) -> None:
        self.colors = np.full(len(xy), self.config.color)
        # center
        centered = xy - (xy.max(axis=0) + xy.min(axis=0)) / 2
        # normalize
        normalized = centered / np.max(np.linalg.norm(centered, axis=1))
        # euclid norm
        self.pattern = np.linalg.norm(normalized, axis=1) * self.config.fineness

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self.colors * self.beat(self.bpm, shift=self.pattern)
