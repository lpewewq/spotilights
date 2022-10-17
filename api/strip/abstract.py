from abc import ABC, abstractmethod

import numpy as np

from ..color import Color


class AbstractStrip(ABC):
    def __init__(self, num_pixels: int, xy: list[tuple[float, float]] = None) -> None:
        super().__init__()
        self.num_pixels = num_pixels
        if xy:
            assert len(xy) == num_pixels
            self.xy = np.array(xy)
        else:
            self.xy = np.linspace([-1, 0], [1, 0], num_pixels)

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
