from colorsys import hsv_to_rgb
from dataclasses import dataclass

from pydantic import BaseModel, conint


def clamp(x):
    return min(255, max(0, int(x)))


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> "Color":
        r, g, b = hsv_to_rgb(h, s, v)
        r = clamp(r * 255)
        g = clamp(g * 255)
        b = clamp(b * 255)
        return Color(r, g, b)

    @classmethod
    def from_int(cls, x: int) -> "Color":
        r = (x >> 16) & 255
        g = (x >> 8) & 255
        b = x & 255
        return Color(r, g, b)

    def as_int(self) -> int:
        r = int(self.r) & 255
        g = int(self.g) & 255
        b = int(self.b) & 255
        return (r << 16) | (g << 8) | b

    def as_bytes(self) -> tuple[int, int, int]:
        r = int(self.r) & 255
        g = int(self.g) & 255
        b = int(self.b) & 255
        return r, g, b

    def blend(self, other: "Color", percentage: float = 0.5) -> "Color":
        keep = 1 - percentage
        r = clamp(self.r * keep + other.r * percentage)
        g = clamp(self.g * keep + other.g * percentage)
        b = clamp(self.b * keep + other.b * percentage)
        return Color(r, g, b)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            r = clamp(self.r + other.r)
            g = clamp(self.g + other.g)
            b = clamp(self.b + other.b)
        else:
            r = clamp(self.r + other)
            g = clamp(self.g + other)
            b = clamp(self.b + other)
        return Color(r, g, b)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            r = clamp(self.r * other.r / 255)
            g = clamp(self.g * other.g / 255)
            b = clamp(self.b * other.b / 255)
        else:
            r = clamp(self.r * other)
            g = clamp(self.g * other)
            b = clamp(self.b * other)
        return Color(r, g, b)


class IntColorModel(BaseModel):
    red: conint(ge=0, le=255)
    green: conint(ge=0, le=255)
    blue: conint(ge=0, le=255)

    def get_color(self) -> Color:
        return Color(r=self.red, g=self.green, b=self.blue)
