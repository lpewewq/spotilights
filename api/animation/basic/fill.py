from ...color import Color
from .bpm import BPMAnimation


class FillAnimation(BPMAnimation):
    def __init__(self, color: Color, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color

    async def on_loop(self) -> None:
        self.strip.fill_color(self.color * self.beat())
