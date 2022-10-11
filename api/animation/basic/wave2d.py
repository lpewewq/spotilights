import numpy as np

from ...color import Color
from ...strip.base import AbstractStrip
from .bpm import BPMAnimation


class Wave2DAnimation(BPMAnimation):
    def __init__(self, color: Color, fineness: float = 30.0, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color
        self.fineness = fineness
        self.origin = np.array([0.0, 0.0])
        self.coords = None
        self.norms = None

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        coords = parent_strip.get_coords()
        # center
        coords = coords - (coords.max(axis=0) + coords.min(axis=0)) / 2
        # normalize
        self.coords = coords / np.max(np.linalg.norm(coords, axis=1))
        self.norms = np.linalg.norm(self.coords - self.origin, axis=1)

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        await super().render(parent_strip, progress)
        for i in range(parent_strip.num_pixels()):
            scale = self.beat(self.norms[i] * self.fineness)
            parent_strip.set_pixel_color(i, self.color * scale)
