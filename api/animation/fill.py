from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from .abstract import AbstractAnimation
from .utils.decorators import on_change


class Fill(AbstractAnimation):
    """Fill with single color."""

    name: Literal["Fill"]
    color: Color = Field(Color(r=0, g=0, b=0), type="color", title="Fill Color")

    def change_callback(self, xy: np.ndarray) -> None:
        self._pattern = np.full(len(xy), self.color)

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self._pattern

    @property
    def needs_spotify(self) -> bool:
        return False
