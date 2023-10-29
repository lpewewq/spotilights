from typing import Literal

import numpy as np
from pydantic import Field

from ..color import Color
from ..spotify.models import Bar, Beat
from .split import Split
from .utils.decorators import on_change
from .utils.ease import EaseFunction, get_ease_function


class Shift(Split):
    """Shift animations on event."""

    name: Literal["Shift"]
    ease_function: EaseFunction = "Quint Out"
    _start = 0
    _duration = 1
    _counter = 0

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._start = beat.start
        self._duration = beat.duration
        self._counter += 1
        # self._counter %= 4
        self.shift_forward()
        return super().on_beat(beat, progress)

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        # width = self.offsets[0][1]
        # start = self.offsets[(self._counter - 1) % len(self.animations)][0]
        # end = self.offsets[self._counter % len(self.animations)][1] - width

        # blend = get_ease_function(self.ease_function)(min(1, (progress - self._start) / self._duration))
        # shift = int(start * (1 - blend) + end * blend)
        shift= 0
        rolled_xy = np.roll(xy, shift=-shift, axis=0)
        pattern = super().render(progress, rolled_xy)
        return np.roll(pattern, shift=shift)
