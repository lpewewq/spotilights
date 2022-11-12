import time
from abc import ABC

import numpy as np
from pydantic import Field, confloat

from ...color import Color
from ...spotify.models import Section
from .sub import MultiSub


class Transition(MultiSub, ABC):
    def __init__(self, config: "Transition.Config") -> None:
        super().__init__(config)
        self.config: Transition.Config
        self.current = 0
        self.next = None
        self.start = 0

    class Config(MultiSub.Config):
        duration: confloat(ge=0, le=1, multiple_of=0.01) = Field(
            0.25, config_type="Numerical", title="Transition Duration", description="s"
        )

    def transition(self, next: int):
        self.next = next
        self.start = time.time()

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        if self.next is not None:
            transition_progress = (time.time() - self.start) / self.config.duration
            if 0 <= transition_progress < 1:
                return Color.lerp(
                    self.animations[self.current].render(progress, xy),
                    self.animations[self.next].render(progress, xy),
                    transition_progress,
                )
            else:
                self.current = self.next
                self.next = None
        return self.animations[self.current].render(progress, xy)


class TransitionOnSection(Transition):
    def on_section(self, section: Section, progress: float) -> None:
        super().on_section(section, progress)
        choices = list(range(len(self.animations)))
        choices.remove(self.current)
        next = np.random.choice(choices, 1)[0]
        self.transition(next)
