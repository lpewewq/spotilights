import numpy as np
from pydantic import confloat

from ...color import Color
from .sub import MultiSub


class Composite(MultiSub):
    def __init__(self, config: "Composite.Config") -> None:
        super().__init__(config)
        self.config: Composite.Config

    class Config(MultiSub.Config):
        percentage: confloat(ge=0.0, le=1.0, multiple_of=0.1) = 0.5

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return Color.lerp(
            self.animations[0].render(progress, xy),
            self.animations[1].render(progress, xy),
            self.config.percentage,
        )
