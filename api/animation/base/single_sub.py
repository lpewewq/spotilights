from abc import ABC

import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip
from .absract import Animation


class SingleSubAnimation(Animation, ABC):
    def __init__(self, animation: Animation) -> None:
        super().__init__()
        self.animation = animation

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.animation})"

    async def on_pause(self, shared_data: SharedData) -> None:
        await self.animation.on_pause(shared_data)

    async def on_resume(self, shared_data: SharedData) -> None:
        await self.animation.on_resume(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        await self.animation.on_track_change(shared_data)

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        await self.animation.on_section(section, progress)

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        await self.animation.on_bar(bar, progress)

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        await self.animation.on_beat(beat, progress)

    async def on_tatum(self, tatum: tk.model.TimeInterval, progress: float) -> None:
        await self.animation.on_tatum(tatum, progress)

    async def on_segment(self, segment: tk.model.Segment, progress: float) -> None:
        await self.animation.on_segment(segment, progress)

    async def render(self, parent_strip: AbstractStrip) -> None:
        await self.animation.render(parent_strip)

    @property
    def depends_on_spotify(self) -> bool:
        return self.animation.depends_on_spotify
