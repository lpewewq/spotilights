from abc import ABC

from ...color import Color
from .absract import Animation


class RainbowAnimation(Animation, ABC):
    def __init__(self, delay: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
