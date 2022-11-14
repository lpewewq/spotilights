from typing import Literal

import numpy as np

from ..spotify.models.audio_analysis import Beat
from .abstract import SingleSub


class Inverse(SingleSub):
    """Container inverting an animation."""

    name: Literal["Inverse"]
    inverse: bool = True

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        colors = super().render(progress, xy)
        if self.inverse:
            return colors[::-1]
        else:
            return colors


class InverseOnBeat(Inverse):
    """Container inverting an animation on every beat."""

    name: Literal["InverseOnBeat"]

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.inverse ^= True
        return super().on_beat(beat, progress)
