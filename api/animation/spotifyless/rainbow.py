import time
from typing import Generator

from ..base import BaseIteratorAnimation


class RainbowAnimation(BaseIteratorAnimation):
    def infinite_generator(self) -> Generator[None, None, None]:
        while True:
            for offset in range(256):
                for i in range(self.strip.num_pixels()):
                    self.strip.set_pixel_color(i, self.rainbow[(i + offset) % 256])

                t = time.time()
                yield
                while (time.time() - t) < self.delay:
                    yield

    @property
    def depends_on_spotify(self) -> bool:
        return False
