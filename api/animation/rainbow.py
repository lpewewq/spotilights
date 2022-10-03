import asyncio
from abc import ABC

from rpi_ws281x import Color

from .base import BaseAnimation


class BaseRainbowAnimation(BaseAnimation, ABC):
    def wheel(self, pos) -> int:
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


class RainbowAnimation(BaseRainbowAnimation):
    def __init__(self, strip: "LEDStrip", delay: float) -> None:
        super().__init__(strip)
        self.delay = delay

    async def loop(self) -> None:
        for j in range(256):
            for i in range(self.strip.numPixels()):
                pos = (int(i * 256 / self.strip.numPixels()) + j) & 255
                self.strip.setPixelColor(i, self.wheel(pos))
            self.strip.show()
            await asyncio.sleep(self.delay)


class TheaterAnimation(BaseRainbowAnimation):
    def __init__(self, strip: "LEDStrip", delay: float) -> None:
        super().__init__(strip)
        self.delay = delay

    async def loop(self) -> None:
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                await asyncio.sleep(self.delay)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
