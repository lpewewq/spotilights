import time
from abc import ABC
from typing import Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from ..spotify.models import Section
from .abstract import MultiSub


class Transition(MultiSub, ABC):
    duration: confloat(ge=0, le=1, multiple_of=0.01) = Field(
        0.25, title="Transition Duration", description="s"
    )
    _current = 0
    _next = None
    _start = 0

    def transition(self, next: int):
        self._next = next
        self._start = time.time()

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        if self._next is not None:
            transition_progress = (time.time() - self._start) / self.duration
            if 0 <= transition_progress < 1:
                return Color.lerp(
                    self.animations[self._current].render(progress, xy),
                    self.animations[self._next].render(progress, xy),
                    transition_progress,
                )
            else:
                self._current = self._next
                self._next = None
        return self.animations[self._current].render(progress, xy)


class TransitionOnSection(Transition):
    """Container animation which randomly transition between animations on section change."""

    class Config:
        title = "Transition"

    name: Literal["TransitionOnSection"]

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_section(self, section: Section, progress: float) -> None:
        choices = list(range(len(self.animations)))
        choices.remove(self._current)
        next = np.random.choice(choices, 1)[0]
        self.transition(next)
        return super().on_section(section, progress)
