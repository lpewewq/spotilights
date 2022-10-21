import numpy as np

from ...color import Color
from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData
from .absract import Animation


class Composite(Animation):
    def __init__(self, animations: list[Animation], percentage: float = 0.5) -> None:
        super().__init__()
        assert len(animations) == 2
        self.animations = animations
        self.percentage = percentage

    def __repr__(self) -> str:
        return type(self).__name__ + f"({len(self.animations)})"

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
        return Color.lerp(self.animations[0].render(progress, xy), self.animations[1].render(progress, xy), self.percentage)

    @property
    def depends_on_spotify(self) -> bool:
        return any(animation.depends_on_spotify for animation in self.animations)
