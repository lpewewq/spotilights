from ...color import Color
from .abstract import AbstractStrip


class SubStrip(AbstractStrip):
    def __init__(
        self,
        strip: AbstractStrip,
        offset: int = 0,
        num_pixels: int = None,
        inverse: bool = False,
    ) -> None:
        super().__init__(num_pixels or strip.num_pixels())
        assert 0 <= offset
        assert offset + self.num_pixels() <= strip.num_pixels()
        self.strip = strip
        self.offset = offset
        self.inverse = inverse

    def get_index(self, i: int) -> int:
        if self.inverse:
            return self.offset + self.num_pixels() - i - 1
        else:
            return self.offset + i

    def get_coord(self, i: int):
        return self.strip.get_coord(self.get_index(i))

    def get_norm(self, i: int) -> float:
        return self.strip.get_norm(self.get_index(i))

    def get_pixel_color(self, i: int) -> Color:
        return self.strip.get_pixel_color(self.get_index(i))

    def set_pixel_color(self, i: int, color: Color) -> None:
        return self.strip.set_pixel_color(self.get_index(i), color)
