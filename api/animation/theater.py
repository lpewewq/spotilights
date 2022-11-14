from typing import Generator, Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color, rainbow
from .iterator import BaseIterator

black = Color(r=0, g=0, b=0)


class Theater(BaseIterator):
    """Theater lights animation."""

    name: Literal["Theater"]
    delay: confloat(ge=0, le=1, multiple_of=0.1) = Field(0.5, config_type="Numerical", title="Delay", description="s")

    @property
    def needs_spotify(self) -> bool:
        return False

    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        n = len(xy)
        for offset in range(256):
            for q in range(3):
                colors = np.full(n, black)
                colors[q::3] = rainbow.take(range(offset, offset + len(colors[q::3])), mode="wrap")
                yield colors, self.delay
