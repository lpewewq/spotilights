from ...color import Color
from .bpm import BPMAnimation


class Wave2DAnimation(BPMAnimation):
    def __init__(self, color: Color, fineness: float = 30.0, low: float = 0, high: float = 1) -> None:
        super().__init__(low, high)
        self.color = color
        self.fineness = fineness

    async def on_loop(self) -> None:
        for i in range(self.strip.num_pixels()):
            norm = self.strip.get_norm(i)
            scale = self.beat(norm * self.fineness)
            self.strip.set_pixel_color(i, self.color * scale)
