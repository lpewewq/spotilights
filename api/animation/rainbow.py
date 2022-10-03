import asyncio

from .base import BaseRainbowAnimation


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
