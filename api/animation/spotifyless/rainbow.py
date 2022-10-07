import time

from ..base import BaseRainbowAnimation


class RainbowAnimation(BaseRainbowAnimation):
    def __init__(self, delay: float) -> None:
        super().__init__(delay)
        self.offset = 0
        self.last_update = time.time()

    async def on_loop(self) -> None:
        now = time.time()
        if (now - self.last_update) < self.delay:
            return
        self.last_update = now

        for i in range(self.strip.num_pixels()):
            self.strip.set_pixel_color(i, self.rainbow[(i + self.offset) % 256])
        self.offset = (self.offset + 1) % 256

    @property
    def depends_on_spotify(self) -> bool:
        return False
