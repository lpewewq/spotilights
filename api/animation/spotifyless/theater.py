from typing import Generator

import numpy as np

from ...color import Color
from ..base import BaseIteratorAnimation


class TheaterAnimation(BaseIteratorAnimation):
    def __init__(self, delay: float) -> None:
        super().__init__()
        self.black = Color(r=0, g=0, b=0)
        self.delay = delay
        self.rainbow = np.array([Color.wheel(pos) for pos in range(256)])


    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        n = len(xy)
        for offset in range(256):
            for q in range(3):
                colors = np.full(n, self.black)
                colors[q::3] = self.rainbow.take(range(offset, offset + len(colors[q::3])), mode="wrap")
                yield colors, self.delay

    @property
    def depends_on_spotify(self) -> bool:
        return False
