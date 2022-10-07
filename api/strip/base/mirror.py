from ...color import Color
from .abstract import AbstractStrip


class MirroredStrip(AbstractStrip):
    def __init__(self, strip: AbstractStrip) -> None:
        super().__init__((strip.num_pixels() + 1) // 2)
        self.strip = strip

    def get_coord(self, i: int):
        return self.strip.get_coord(i)

    def get_norm(self, i: int) -> float:
        return self.strip.get_norm(i)

    def get_pixel_color(self, i: int) -> Color:
        return self.strip.get_pixel_color(i)

    def set_pixel_color(self, i: int, color: Color) -> None:
        self.strip.set_pixel_color(i, color)
        self.strip.set_pixel_color(self.strip.num_pixels() - i - 1, color)
