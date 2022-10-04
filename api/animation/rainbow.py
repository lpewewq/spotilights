import asyncio

from fastapi import Body

from ..spotify import spotify_animator
from . import router
from .base import BaseRainbowAnimation


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    await spotify_animator.start(RainbowAnimation, delay)


class RainbowAnimation(BaseRainbowAnimation):
    async def on_loop(self) -> None:
        for offset in range(256):
            for i in range(self.strip.num_pixels()):
                self.strip.set_pixel_color(i, self.rainbow[(i + offset) % 256])
            self.strip.show()
            await asyncio.sleep(self.delay)
