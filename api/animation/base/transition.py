import time
from abc import ABC

import numpy as np

from ...color import Color
from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData
from .abstract import Animation, AnimationModel


class Transition(Animation, ABC):
    def __init__(self, config: "Transition.Config" = None) -> None:
        super().__init__(config)
        self.config: Transition.Config
        self.animations: list[Animation] = [animation.construct() for animation in self.config.sub]
        self.current = self.config.start
        self.next = None
        self.start = 0

    class Config(Animation.Config):
        sub: list[AnimationModel]
        start: int = 0
        duration: float = 0.25

    def transition(self, next: int):
        self.next = next
        self.start = time.time()

    async def on_pause(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_pause(shared_data)

    async def on_resume(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_resume(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_track_change(shared_data)

    def on_section(self, section: Section, progress: float) -> None:
        for animation in self.animations:
            animation.on_section(section, progress)

    def on_bar(self, bar: Bar, progress: float) -> None:
        for animation in self.animations:
            animation.on_bar(bar, progress)

    def on_beat(self, beat: Beat, progress: float) -> None:
        for animation in self.animations:
            animation.on_beat(beat, progress)

    def on_tatum(self, tatum: Tatum, progress: float) -> None:
        for animation in self.animations:
            animation.on_tatum(tatum, progress)

    def on_segment(self, segment: Segment, progress: float) -> None:
        for animation in self.animations:
            animation.on_segment(segment, progress)

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

    @property
    def depends_on_spotify(self) -> bool:
        return any(animation.depends_on_spotify for animation in self.animations)


class TransitionOnSection(Transition):
    def on_section(self, section: Section, progress: float) -> None:
        super().on_section(section, progress)
        choices = list(range(len(self.animations)))
        choices.remove(self.current)
        next = np.random.choice(choices, 1)[0]
        self.transition(next)
