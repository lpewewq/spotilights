from colorsys import hsv_to_rgb
from dataclasses import dataclass

import numpy as np
from pydantic import conint


def clamp(x):
    return min(255, max(0, int(x)))


@dataclass
class Color:
    r: conint(ge=0, le=255, multiple_of=1) = 0
    g: conint(ge=0, le=255, multiple_of=1) = 0
    b: conint(ge=0, le=255, multiple_of=1) = 0

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> "Color":
        r, g, b = hsv_to_rgb(h, s, v)
        r = clamp(r * 255)
        g = clamp(g * 255)
        b = clamp(b * 255)
        return Color(r, g, b)

    @classmethod
    def wheel(cls, pos: int) -> "Color":
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(r=pos * 3, g=255 - pos * 3, b=0)
        elif pos < 170:
            pos -= 85
            return Color(r=255 - pos * 3, g=0, b=pos * 3)
        else:
            pos -= 170
            return Color(r=0, g=pos * 3, b=255 - pos * 3)

    def as_int(self) -> int:
        r = clamp(self.r)
        g = clamp(self.g)
        b = clamp(self.b)
        return (r << 16) | (g << 8) | b

    def as_bytes(self) -> tuple[int, int, int]:
        r = clamp(self.r)
        g = clamp(self.g)
        b = clamp(self.b)
        return r, g, b

    @classmethod
    def lerp(cls, a: "Color", b: "Color", percentage: float = 0.5) -> "Color":
        return a * (1 - percentage) + b * percentage

    def __add__(self, other):
        if isinstance(other, self.__class__):
            r = self.r + other.r
            g = self.g + other.g
            b = self.b + other.b
        else:
            r = self.r + other
            g = self.g + other
            b = self.b + other
        return Color(r, g, b)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            r = self.r - other.r
            g = self.g - other.g
            b = self.b - other.b
        else:
            r = self.r - other
            g = self.g - other
            b = self.b - other
        r = clamp(r)
        g = clamp(g)
        b = clamp(b)
        return Color(r, g, b)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            r = self.r * other.r / 255
            g = self.g * other.g / 255
            b = self.b * other.b / 255
        else:
            r = self.r * other
            g = self.g * other
            b = self.b * other
        return Color(r, g, b)

    def __rmul__(self, other):
        return self * other


rainbow = np.array([Color.wheel(pos) for pos in range(256)])
