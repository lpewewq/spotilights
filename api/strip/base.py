from abc import ABC, abstractmethod
from typing import List

from ..color import Color


class LEDStrip(ABC):
    @abstractmethod
    def show(self) -> None:
        """Update LED strip"""

    @abstractmethod
    def get_pixel_color(self, n: int) -> Color:
        """Get pixel color"""

    @abstractmethod
    def set_pixel_color(self, n: int, color: Color) -> None:
        """Set color of LED at position n"""

    @abstractmethod
    def get_pixels(self) -> List[Color]:
        """Get all pixel colors"""

    @abstractmethod
    def get_brightness(self) -> int:
        """Get LED Strip brightness [0, 255]"""

    @abstractmethod
    def set_brightness(self, brightness: int) -> None:
        """Set LED Strip brightness [0, 255]"""

    @abstractmethod
    def num_pixels(self) -> int:
        """Number of pixels in the strip"""

    def clear(self) -> None:
        """Clear the strip"""
        self.fill_color(Color(r=0, g=0, b=0))
        self.show()

    def fill_color(self, color: Color) -> None:
        """Fill enitre strip with single color"""
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)

    def add_pixel_color(self, n: int, color: Color) -> None:
        """Add color to LED at position n"""
        self.set_pixel_color(n, self.get_pixel_color(n) + color)

    def mult_pixel_color(self, n: int, color: Color) -> None:
        """Scale color of LED at position n"""
        self.set_pixel_color(n, self.get_pixel_color(n) * s)
