from abc import ABC, abstractmethod
from typing import List

from colour import Color


class LEDStrip(ABC):
    def clear(self) -> None:
        self.fill_color(Color("black"))
        self.show()

    def fill_color(self, color: Color) -> None:
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)

    @abstractmethod
    def show(self) -> None:
        """Update LED strip"""

    @abstractmethod
    def set_pixel_color(self, n: int, color: Color) -> None:
        """Set color of LED at position n"""

    @abstractmethod
    def get_brightness(self) -> int:
        """Get LED Strip brightness [0, 255]"""

    @abstractmethod
    def set_brightness(self, brightness: int) -> None:
        """Set LED Strip brightness [0, 255]"""

    @abstractmethod
    def get_pixels(self) -> List[Color]:
        """Get all pixel colors"""

    @abstractmethod
    def num_pixels(self) -> int:
        """Number of pixels in the strip"""

    @abstractmethod
    def get_pixel_color(self, n) -> Color:
        """Get pixel color"""
