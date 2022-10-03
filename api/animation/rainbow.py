import asyncio

from colour import Color
from fastapi import Body

from . import animator, router
from .base import BaseRainbowAnimation


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    animator.start(RainbowAnimation, delay)


class RainbowAnimation(BaseRainbowAnimation):
    async def loop(self) -> None:
        for j in range(256):
            for i in range(self.strip.num_pixels()):
                pos = (int(i * 256 / self.strip.num_pixels()) + j) & 255
                r, g, b = self.wheel(pos)
                color = Color(rgb=(r / 255, g / 255, b / 255))
                self.strip.set_pixel_color(i, color)
            self.strip.show()
            await asyncio.sleep(self.delay)
