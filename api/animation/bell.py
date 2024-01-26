from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from .abstract import AbstractAnimation
from .utils import bell
from .utils.decorators import on_change


class Bell(AbstractAnimation):
    """Bell Curve."""

    name: Literal["Bell"]
    color: Color = Field(Color(r=255), type="color", title="Fill Color")
    width: confloat(ge=0, le=100, multiple_of=1) = Field(10.0, title="Width", description=" ")

    def change_callback(self, xy: np.ndarray) -> None:
        arange = np.linspace(-self.width, self.width, num=len(xy))
        self._pattern = bell(arange) * self.color

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self._pattern

    @property
    def needs_spotify(self) -> bool:
        return False
