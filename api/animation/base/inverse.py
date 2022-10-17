import numpy as np

from .absract import Animation
from .sub import SingleSubAnimation


class InverseAnimation(SingleSubAnimation):
    def __init__(self, animation: Animation, inverse=True) -> None:
        super().__init__(animation)
        self.inverse = inverse

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        colors = super().render(progress, xy)
        if self.inverse:
            return colors[::-1]
        else:
            return colors
