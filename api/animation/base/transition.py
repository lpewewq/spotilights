import time
from abc import ABC

import numpy as np

from ...color import Color
from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData
from .absract import Animation


class Transition(Animation, ABC):
    def __init__(self, animations: list[Animation], start: int = 0) -> None:
        super().__init__()
        self.animations = animations
        self.current = start
        self.next = None
        self.start = 0
        self.duration = 1

    def __repr__(self) -> str:
        return type(self).__name__ + f"({len(self.animations)} {self.animations[self.current]})"

    def transition(self, next: int, duration: float = 1):
        self.next = next
        self.duration = duration
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
            transition_progress = (time.time() - self.start) / self.duration
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
        next = (self.current + 1) % len(self.animations)
        self.transition(next)
