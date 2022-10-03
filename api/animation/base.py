import asyncio
from abc import ABC, abstractmethod

from ..strip.base import LEDStrip


class BaseAnimation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    def __init__(self, strip: LEDStrip) -> None:
        self.strip: LEDStrip = strip

    async def start(self) -> None:
        try:
            while True:
                await self.loop()
                await asyncio.sleep(0)
        except Exception as e:
            print(f"{self} excepted:", e)

    @abstractmethod
    async def loop(self) -> None:
        """Animation loop"""


class BaseRainbowAnimation(BaseAnimation, ABC):
    def __init__(self, strip: LEDStrip, delay: float) -> None:
        super().__init__(strip)
        self.delay = delay

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return pos * 3, 255 - pos * 3, 0
        elif pos < 170:
            pos -= 85
            return 255 - pos * 3, 0, pos * 3
        else:
            pos -= 170
            return 0, pos * 3, 255 - pos * 3
