from typing import Generator

import numpy as np

from ...color import Color
from ..base import BaseIterator


class Rainbow(BaseIterator):
    def __init__(self, delay: float) -> None:
        super().__init__()
        self.delay = delay
        self.rainbow = np.array([Color.wheel(pos) for pos in range(256)])

    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        for offset in range(256):
            yield self.rainbow.take(range(offset, offset + len(xy)), mode="wrap"), self.delay

    @property
    def depends_on_spotify(self) -> bool:
        return False
