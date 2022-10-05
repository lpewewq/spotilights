import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import SubStrip
from .absract import Animation


class SplitAnimation(Animation):
    def __init__(
        self, left_animation: Animation, right_animation: Animation, ratio: float = 0.5
    ) -> None:
        super().__init__()
        self.left_animation = left_animation
        self.right_animation = right_animation
        self.ratio = ratio

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.left_animation}, {self.right_animation})"

    def init_strip(self, strip: SubStrip) -> None:
        super().init_strip(strip)
        n = strip.num_pixels()
        num_pixels_left = int(self.ratio * n)
        num_pixels_right = n - num_pixels_left
        self.left_animation.init_strip(
            SubStrip(strip=strip, num_pixels=num_pixels_left)
        )
        self.right_animation.init_strip(
            SubStrip(
                strip=strip,
                offset=num_pixels_left,
                num_pixels=num_pixels_right,
                inverse=True,
            )
        )

    async def on_loop(self) -> None:
        await self.left_animation.on_loop()
        await self.right_animation.on_loop()

    async def on_pause(self, shared_data: SharedData) -> None:
        await self.left_animation.on_pause(shared_data)
        await self.right_animation.on_pause(shared_data)

    async def on_resume(self, shared_data: SharedData) -> None:
        await self.left_animation.on_resume(shared_data)
        await self.right_animation.on_resume(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        await self.left_animation.on_track_change(shared_data)
        await self.right_animation.on_track_change(shared_data)

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        await self.left_animation.on_section(section, progress)
        await self.right_animation.on_section(section, progress)

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        await self.left_animation.on_bar(bar, progress)
        await self.right_animation.on_bar(bar, progress)

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        tmp = self.left_animation.strip
        self.left_animation.strip = self.right_animation.strip
        self.right_animation.strip = tmp
        await self.left_animation.on_beat(beat, progress)
        await self.right_animation.on_beat(beat, progress)

    async def on_tatum(self, tatum: tk.model.TimeInterval, progress: float) -> None:
        await self.left_animation.on_tatum(tatum, progress)
        await self.right_animation.on_tatum(tatum, progress)

    async def on_segment(self, segment: tk.model.Segment, progress: float) -> None:
        await self.left_animation.on_segment(segment, progress)
        await self.right_animation.on_segment(segment, progress)
