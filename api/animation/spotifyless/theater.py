import time
from typing import Generator

from ...color import Color
from ..base import BaseIteratorAnimation


class TheaterAnimation(BaseIteratorAnimation):
    black = Color(r=0, g=0, b=0)

    def generator(self) -> Generator[float, None, None]:
        for offset in range(256):
            for q in range(3):
                for i in range(0, self.strip.num_pixels(), 3):
                    pos = i + q
                    if pos < self.strip.num_pixels():
                        self.strip.set_pixel_color(pos, self.rainbow[(i + offset) % 256])
                yield self.delay
                for i in range(0, self.strip.num_pixels(), 3):
                    pos = i + q
                    if pos < self.strip.num_pixels():
                        self.strip.set_pixel_color(pos, self.black)

    @property
    def depends_on_spotify(self) -> bool:
        return False
