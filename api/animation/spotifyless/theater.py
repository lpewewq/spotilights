import time

from ...color import Color
from ..base import BaseRainbowAnimation


class TheaterAnimation(BaseRainbowAnimation):
    def __init__(self, delay: float) -> None:
        super().__init__(delay)
        self.black = Color(r=0, g=0, b=0)
        self.offset = 0
        self.q = 0
        self.last_update = time.time()

    async def on_loop(self) -> None:
        now = time.time()
        if (now - self.last_update) < self.delay:
            return
        self.last_update = now

        for i in range(0, self.strip.num_pixels(), 3):
            pos = i + self.q
            if pos < self.strip.num_pixels():
                self.strip.set_pixel_color(pos, self.black)

        self.q = (self.q + 1) % 3

        for i in range(0, self.strip.num_pixels(), 3):
            pos = i + self.q
            if pos < self.strip.num_pixels():
                self.strip.set_pixel_color(pos, self.rainbow[(i + self.offset) % 256])

        if self.q == 0:
            self.offset = (self.offset + 1) % 256

    @property
    def depends_on_spotify(self) -> bool:
        return False
