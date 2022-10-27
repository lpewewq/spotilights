from typing import Generator

import numpy as np
from pydantic import confloat

from ...color import Color
from ..base import BaseIterator


class Theater(BaseIterator):
    rainbow = np.array([Color.wheel(pos) for pos in range(256)])
    black = Color(r=0, g=0, b=0)

    def __init__(self, config: "Theater.Config") -> None:
        super().__init__(config)
        self.config: Theater.Config

    class Config(BaseIterator.Config):
        delay: confloat(ge=0) = 0.5

        @property
        def needs_spotify(self) -> bool:
            return False

    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        n = len(xy)
        for offset in range(256):
            for q in range(3):
                colors = np.full(n, self.black)
                colors[q::3] = self.rainbow.take(range(offset, offset + len(colors[q::3])), mode="wrap")
                yield colors, self.config.delay
