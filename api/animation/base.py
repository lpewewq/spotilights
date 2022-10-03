from abc import ABC, abstractmethod

from rpi_ws281x import Color


class BaseAnimation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    def __init__(self, strip: "LEDStrip") -> None:
        self.strip = strip

    @abstractmethod
    async def loop(self) -> None:
        """Animation loop"""

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
