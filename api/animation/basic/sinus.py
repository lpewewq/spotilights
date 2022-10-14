import numpy as np

from ...color import Color
from ...strip.base import AbstractStrip
from .bpm import BPMAnimation


class SinusAnimation(BPMAnimation):
    def __init__(self, color: Color, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        n = parent_strip.num_pixels()
        bell = lambda i: (0.1 + 0.9 / np.sqrt(1 + (i - n) ** 2))
        self.pattern1 = [self.color * bell(i) for i in range(2 * n + 1)]

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        await super().render(parent_strip, progress)
        n = parent_strip.num_pixels()
        offset1 = round(self.beat(self.bpm / 2) * n)
        for i in range(n):
            c = self.pattern1[offset1 + i]
            parent_strip.set_pixel_color(i, c)
