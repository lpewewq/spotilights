from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from .abstract import AbstractAnimation
from .utils.decorators import on_change


class Test2D(AbstractAnimation):
    """2D Test animation."""

    name: Literal["Test2D"]
    color1: Color = Field(Color(r=255), type="color", title="Fill Color")
    color2: Color = Field(Color(b=255), type="color", title="Fill Color")

    def change_elements_callback(self, xy: np.ndarray) -> None:
        transformed = xy / 2 + [0.5, 0.5]
        self.pattern = transformed @ np.array([self.color1, self.color2])

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self.pattern

    @property
    def needs_spotify(self) -> bool:
        return False
