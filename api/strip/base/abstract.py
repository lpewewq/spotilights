from abc import ABC, abstractmethod

import numpy as np

from ...color import Color


class AbstractStrip(ABC):
    def __init__(self, num_pixels: int) -> None:
        super().__init__()
        assert num_pixels > 0
        self._num_pixels = num_pixels

    @abstractmethod
    def get_coord(self, i: int):
        """Get 2D coordinates of pixel i"""

    @abstractmethod
    def get_norm(self, i: int) -> float:
        """Get 2D distance to origin of pixel i"""

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
            # center
            self._coords = self._coords - (self._coords.max(axis=0) - self._coords.min(axis=0)) / 2
            # normalize
            self._coords = self._coords / np.max(np.linalg.norm(self._coords, axis=1))
        else:
            self._coords = np.linspace([-1, 0], [1,0],num_pixels)
        self._norms = np.linalg.norm(self._coords, axis=1)

    def get_coord(self, i: int):
        return self._coords[i]

    def get_norm(self, i: int) -> float:
        return self._norms[i]

    @abstractmethod
    def show(self) -> None:
        """Update LED strip"""

    @abstractmethod
    def get_brightness(self) -> int:
        """Get LED Strip brightness [0, 255]"""

    @abstractmethod
    def set_brightness(self, brightness: int) -> None:
        """Set LED Strip brightness [0, 255]"""
