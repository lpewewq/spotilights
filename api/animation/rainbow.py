import time

from fastapi import Body

from ..spotify import spotify_animator
from . import router
from .base import RainbowAnimation


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    animation = RainbowAnimation(delay)
    await spotify_animator.start(animation)


class RainbowAnimation(RainbowAnimation):
    def __init__(self, delay: float, *args, **kwargs) -> None:
        super().__init__(delay, *args, **kwargs)
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
