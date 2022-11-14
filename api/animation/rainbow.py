from typing import Generator, Literal

import numpy as np
from pydantic import Field, confloat

from ..color import rainbow
from .iterator import BaseIterator


class Rainbow(BaseIterator):
    """Simple cycling rainbow animation."""

    name: Literal["Rainbow"]
    delay: confloat(ge=0, le=1, multiple_of=0.1) = Field(0.5, config_type="Numerical", title="Delay", description="s")

    @property
    def needs_spotify(self) -> bool:
        return False

    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        for offset in range(256):
            yield rainbow.take(range(offset, offset + len(xy)), mode="wrap"), self.delay
