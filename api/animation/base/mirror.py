import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip, MirroredStrip
from .absract import Animation


class MirrorAnimation(Animation):
    def __init__(self, animation: Animation, divisions: int = 2, inverse: list[bool] = None) -> None:
        super().__init__()
        self.animation = animation
        self.divisions = divisions
        self.inverse = inverse

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.animation})"

    def init_strip(self, strip: AbstractStrip) -> None:
        super().init_strip(strip)
        self.animation.init_strip(MirroredStrip(strip=strip, divisions=self.divisions, inverse=self.inverse))

    async def on_loop(self) -> None:
        await self.animation.on_loop()

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

    @property
    def depends_on_spotify(self) -> bool:
        return self.animation.depends_on_spotify
