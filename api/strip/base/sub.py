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
        super().__init__()
        self._strip = strip
        self._offset = offset
        self._num_pixels = num_pixels or strip.num_pixels()
        self._inverse = inverse
        assert self._num_pixels <= strip.num_pixels()
        assert self._offset + self._num_pixels <= strip.num_pixels()

    def num_pixels(self) -> int:
        return self._num_pixels

    def get_pixel_color(self, n: int) -> Color:
        if self._inverse:
            return self._strip.get_pixel_color(self._offset + self._num_pixels - n - 1)
        else:
            return self._strip.get_pixel_color(self._offset + n)

    def set_pixel_color(self, n: int, color: Color) -> None:
        if self._inverse:
            return self._strip.set_pixel_color(
                self._offset + self._num_pixels - n - 1, color
            )
        else:
            return self._strip.set_pixel_color(self._offset + n, color)
