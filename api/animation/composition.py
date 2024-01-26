from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from .abstract import MultiSub


class Composite(MultiSub):
    """Container compositing two animations."""

    name: Literal["Composite"]
    blend: confloat(ge=0.0, le=1.0, multiple_of=0.1) = Field(0.5, title="Blend", description="%")

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return Color.lerp(
            self.animations[0].render(progress, xy),
            self.animations[1].render(progress, xy),
            self.blend,
        )
