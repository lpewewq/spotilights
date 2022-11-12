from typing import Generator

import numpy as np
from pydantic import Field, confloat

from ...color import Color
from ..base import BaseIterator


class Rainbow(BaseIterator):
    rainbow = np.array([Color.wheel(pos) for pos in range(256)])

    def __init__(self, config: "Rainbow.Config") -> None:
        super().__init__(config)
        self.config: Rainbow.Config

    class Config(BaseIterator.Config):
        delay: confloat(ge=0, le=1, multiple_of=0.1) = Field(0.5, config_type="Numerical", title="Delay", description="s")

        @property
        def needs_spotify(self) -> bool:
            return False

    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        for offset in range(256):
            yield self.rainbow.take(range(offset, offset + len(xy)), mode="wrap"), self.config.delay
