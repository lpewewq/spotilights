from ...color import Color
from ...strip.base import AbstractStrip
from .bpm import BPMAnimation


class Wave2DAnimation(BPMAnimation):
    def __init__(self, color: Color, fineness: float = 30.0, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color
        self.fineness = fineness

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    async def render(self, parent_strip: AbstractStrip) -> None:
        await super().render(parent_strip)
        for i in range(parent_strip.num_pixels()):
            norm = parent_strip.get_norm(i)
            scale = self.beat(norm * self.fineness)
            parent_strip.set_pixel_color(i, self.color * scale)
