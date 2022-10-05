from ...color import Color
from .abstract import AbstractStrip


class MirroredStrip(AbstractStrip):
    def __init__(self, strip: AbstractStrip) -> None:
        super().__init__()
        self.strip = strip
        self.total_num_pixels = strip.num_pixels()
        self.half_num_pixels = (self.total_num_pixels + 1) // 2

    def num_pixels(self) -> int:
        return self.half_num_pixels

    def get_pixel_color(self, n: int) -> Color:
        return self.strip.get_pixel_color(n)

    def set_pixel_color(self, n: int, color: Color) -> None:
        self.strip.set_pixel_color(n, color)
        self.strip.set_pixel_color(self.total_num_pixels - n - 1, color)
