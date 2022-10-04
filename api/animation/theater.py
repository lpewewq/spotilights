import asyncio

from fastapi import Body

from ..color import Color
from ..strip.base import LEDStrip
from . import animator, router
from .base import BaseRainbowAnimation


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    animator.start(TheaterAnimation, delay)


class TheaterAnimation(BaseRainbowAnimation):
    def __init__(self, strip: LEDStrip, delay: float) -> None:
        super().__init__(strip, delay)
        self.black = Color(r=0, g=0, b=0)

    async def loop(self) -> None:
        for offset in range(256):
            for q in range(3):
                for i in range(0, self.strip.num_pixels(), 3):
                    self.strip.set_pixel_color(i + q, self.rainbow[(i + offset) % 256])
                self.strip.show()
                await asyncio.sleep(self.delay)
                for i in range(0, self.strip.num_pixels(), 3):
                    self.strip.set_pixel_color(i + q, self.black)
