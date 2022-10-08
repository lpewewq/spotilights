from ...color import Color
from ...strip.base import AbstractStrip
from .bpm import BPMAnimation


class FillAnimation(BPMAnimation):
    def __init__(self, color: Color, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    async def render(self, parent_strip: AbstractStrip) -> None:
        await super().render(parent_strip)
        parent_strip.fill_color(self.color * self.beat())
