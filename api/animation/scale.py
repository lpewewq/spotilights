from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from ..spotify.models import Bar, Beat
from .abstract import SingleSub
from .utils import bell
from .utils.decorators import on_change
from .utils.ease import EaseFunction, get_ease_function


class BeatScale(SingleSub):
    """Scale animation on beat."""

    name: Literal["BeatScale"]
    ease_function: EaseFunction = "Sinus In & Out"
    _start = 0
    _duration = 1

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._start = beat.start
        self._duration = beat.duration
        return super().on_beat(beat, progress)

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        scaling = min(1, (progress - self._start) / self._duration)
        scaling = get_ease_function(self.ease_function)(scaling)
        return super().render(progress, xy) * scaling

    @property
    def needs_spotify(self) -> bool:
        return True
