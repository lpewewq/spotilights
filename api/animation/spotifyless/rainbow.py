import time
from typing import Generator

from ...strip.base import AbstractStrip
from ..base import BaseIteratorAnimation


class RainbowAnimation(BaseIteratorAnimation):
    def generator(self, strip: AbstractStrip) -> Generator[float, None, None]:
        for offset in range(256):
            for i in range(strip.num_pixels()):
                strip.set_pixel_color(i, self.rainbow[(i + offset) % 256])
            yield self.delay

    @property
    def depends_on_spotify(self) -> bool:
        return False
