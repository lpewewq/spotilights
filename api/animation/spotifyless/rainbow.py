import time
from typing import Generator

from ..base import BaseIteratorAnimation


class RainbowAnimation(BaseIteratorAnimation):
    def generator(self) -> Generator[float, None, None]:
        for offset in range(256):
            for i in range(self.strip.num_pixels()):
                self.strip.set_pixel_color(i, self.rainbow[(i + offset) % 256])
            yield self.delay

    @property
    def depends_on_spotify(self) -> bool:
        return False
