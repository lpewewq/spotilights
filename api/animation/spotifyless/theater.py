import time
from typing import Generator

from ...color import Color
from ...strip.base import AbstractStrip
from ..base import BaseIteratorAnimation


class TheaterAnimation(BaseIteratorAnimation):
    black = Color(r=0, g=0, b=0)

    def generator(self, strip: AbstractStrip) -> Generator[float, None, None]:
        for offset in range(256):
            for q in range(3):
                for i in range(0, strip.num_pixels(), 3):
                    pos = i + q
                    if pos < strip.num_pixels():
                        strip.set_pixel_color(pos, self.rainbow[(i + offset) % 256])
                yield self.delay
                for i in range(0, strip.num_pixels(), 3):
                    pos = i + q
                    if pos < strip.num_pixels():
                        strip.set_pixel_color(pos, self.black)

    @property
    def depends_on_spotify(self) -> bool:
        return False
