from abc import ABC, abstractmethod

import numpy as np

from ..color import Color


class AbstractStrip(ABC):
    def __init__(self, num_pixels: int, xy: np.ndarray) -> None:
        super().__init__()
        self.num_pixels = num_pixels
        self.xy = xy

    def clear(self):
        self.show(np.full(self.num_pixels, Color()))

    @abstractmethod
    def show(self, colors: np.ndarray) -> None:
        """Update LED strip"""

    @abstractmethod
    def get_brightness(self) -> int:
        """Get LED Strip brightness [0, 255]"""

    @abstractmethod
    def set_brightness(self, brightness: int) -> None:
        """Set LED Strip brightness [0, 255]"""
