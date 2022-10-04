from colorsys import hsv_to_rgb
from dataclasses import dataclass

from pydantic import BaseModel, confloat, conint


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> "Color":
        r, g, b = hsv_to_rgb(h, s, v)
        r = int(r * 255) & 255
        g = int(g * 255) & 255
        b = int(b * 255) & 255
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

    def scale(self, f: float) -> "Color":
        r = int(self.r * f) & 255
        g = int(self.g * f) & 255
        b = int(self.b * f) & 255
        return Color(r, g, b)

    def blend(self, other: "Color", f: float = 0.5) -> "Color":
        keep = 1 - f
        r = int(self.r * keep + other.r * f) & 255
        g = int(self.g * keep + other.g * f) & 255
        b = int(self.b * keep + other.b * f) & 255
        return Color(r, g, b)


class IntColorModel(BaseModel):
    red: conint(ge=0, le=255)
    green: conint(ge=0, le=255)
    blue: conint(ge=0, le=255)

    def get_color(self) -> Color:
        return Color(r=self.red, g=self.green, b=self.blue)
