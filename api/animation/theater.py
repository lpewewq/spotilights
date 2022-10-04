import asyncio

from fastapi import Body

from ..color import Color
from ..spotify import spotify_animator
from . import router
from .base import BaseRainbowAnimation


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    await spotify_animator.start(TheaterAnimation, delay)


class TheaterAnimation(BaseRainbowAnimation):
    black = Color(r=0, g=0, b=0)

    async def on_loop(self) -> None:
        for offset in range(256):
            for q in range(3):
                for i in range(0, self.strip.num_pixels(), 3):
                    self.strip.set_pixel_color(i + q, self.rainbow[(i + offset) % 256])
                self.strip.show()
                await asyncio.sleep(self.delay)
                for i in range(0, self.strip.num_pixels(), 3):
                    self.strip.set_pixel_color(i + q, self.black)
