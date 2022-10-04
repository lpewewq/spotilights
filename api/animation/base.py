import asyncio
import traceback
from abc import ABC, abstractmethod

from ..color import Color
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
            traceback.print_exc()

    @abstractmethod
    async def loop(self) -> None:
        """Animation loop"""


class BaseRainbowAnimation(BaseAnimation, ABC):
    def __init__(self, strip: LEDStrip, delay: float) -> None:
        super().__init__(strip)
        self.delay = delay
        self.rainbow = [self.wheel(pos) for pos in range(256)]

    def wheel(self, pos: int) -> Color:
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(r=pos * 3, g=255 - pos * 3, b=0)
        elif pos < 170:
            pos -= 85
            return Color(r=255 - pos * 3, g=0, b=pos * 3)
        else:
            pos -= 170
            return Color(r=0, g=pos * 3, b=255 - pos * 3)
