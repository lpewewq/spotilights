import numpy as np

from ...color import Color
from .abstract import AbstractStrip


class MirroredStrip(AbstractStrip):
    def __init__(self, strip: AbstractStrip, divisions: int = 2, inverse: list[bool] = None) -> None:
        super().__init__((strip.num_pixels() + divisions - 1) // divisions)
        assert divisions > 0
        self.strip = strip
        self.divisions = divisions
        if inverse is None:
            self.inverse = [i % 2 == 1 for i in range(divisions)]
        else:
            assert len(inverse) == divisions
            self.inverse = inverse
        self.offsets = [round((i * strip.num_pixels()) / divisions) for i in range(divisions + 1)]

    def get_coord(self, i: int) -> np.ndarray:
        return self.strip.get_coord(i)

    def get_coords(self) -> np.ndarray:
        return self.strip.get_coords()[:self.num_pixels()]

    def get_pixel_color(self, i: int) -> Color:
        return self.strip.get_pixel_color(i)

    def set_pixel_color(self, i: int, color: Color) -> None:
        for d in range(self.divisions):
            if self.inverse[d]:
                self.strip.set_pixel_color(self.offsets[d + 1] - i - 1, color)
            else:
                self.strip.set_pixel_color(self.offsets[d] + i, color)
