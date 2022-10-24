import numpy as np

from ...color import Color
from ..base.decorators import on_change
from .bpm import BPM


class Sinus(BPM):
    def __init__(self, config: "Sinus.Config" = None) -> None:
        super().__init__(config)
        self.config: Sinus.Config

    class Config(BPM.Config):
        color: Color = Color(r=255)

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        bell = lambda i: (0.1 + 0.9 / np.sqrt(1 + (i - n) ** 2))
        colors = np.full(2 * n + 1, self.config.color)
        self.pattern = colors * bell(np.arange(2 * n + 1))

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat = self.beat(self.bpm / 2)
        offset = round(beat * n)
        return self.pattern[offset : offset + n]
