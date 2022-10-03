import asyncio
from abc import ABC

from colour import Color
from fastapi import Body

from . import animator, router
from .base import BaseRainbowAnimation


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    animator.start(TheaterAnimation, delay)


class TheaterAnimation(BaseRainbowAnimation):
    async def loop(self) -> None:
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.num_pixels(), 3):
                    r, g, b = self.wheel((i + j) % 255)
                    color = Color(rgb=(r / 255, g / 255, b / 255))
                    self.strip.set_pixel_color(i + q, color)
                self.strip.show()
                await asyncio.sleep(self.delay)
                for i in range(0, self.strip.num_pixels(), 3):
                    self.strip.set_pixel_color(i + q, Color("black"))
