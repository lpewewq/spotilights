from abc import ABC, abstractmethod

import numpy as np

from ...color import Color


class AbstractStrip(ABC):
    def __init__(self, num_pixels: int) -> None:
        super().__init__()
        assert num_pixels > 0
        self._num_pixels = num_pixels

    @abstractmethod
    def get_coord(self, i: int) -> np.ndarray:
        """Get 2D coordinates of pixel i"""

    @abstractmethod
    def get_coords(self) -> np.ndarray:
        """Get 2D coordinates of all pixels"""

    @abstractmethod
    def get_pixel_color(self, i: int) -> Color:
        """Get pixel color"""

    @abstractmethod
    def set_pixel_color(self, i: int, color: Color) -> None:
        """Set color of LED at position i"""

    def num_pixels(self) -> int:
        """Number of pixels in the strip"""
        return self._num_pixels

    def get_pixels(self) -> list[Color]:
        """Get all pixel colors"""
        return [self.get_pixel_color(i) for i in range(self.num_pixels())]

    def clear(self) -> None:
        """Clear the strip"""
        self.fill_color(Color(r=0, g=0, b=0))

    def fill_color(self, color: Color) -> None:
        """Fill enitre strip with single color"""
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)

    def add_pixel_color(self, i: int, color: Color) -> None:
        """Add color to LED at position i"""
        self.set_pixel_color(i, self.get_pixel_color(i) + color)

    def mult_pixel_color(self, i: int, color: Color) -> None:
        """Scale color of LED at position i"""
        self.set_pixel_color(i, self.get_pixel_color(i) * color)


class GlobalStrip(AbstractStrip, ABC):
    def __init__(self, num_pixels: int, xy: list[tuple[float, float]] = None) -> None:
        super().__init__(num_pixels)
        if xy:
            assert len(xy) == num_pixels
            self._coords = np.array(xy)
        else:
            self._coords = np.linspace([-1, 0], [1,0],num_pixels)

    def get_coord(self, i: int) -> np.ndarray:
        return self._coords[i]

    def get_coords(self) -> np.ndarray:
        return self._coords

    @abstractmethod
    def show(self) -> None:
        """Update LED strip"""

    @abstractmethod
    def get_brightness(self) -> int:
        """Get LED Strip brightness [0, 255]"""

    @abstractmethod
    def set_brightness(self, brightness: int) -> None:
        """Set LED Strip brightness [0, 255]"""
