from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from .bpm import BPM


class Fill(BPM):
    """Flash on beat."""

    name: Literal["Fill"]
    color: Color = Field(Color(r=255), config_type="Color", title="Fill Color")

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        color = self.color * self.beat(self._bpm)
        return np.full(len(xy), color)
