from collections import deque

import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip, SubStrip
from .absract import Animation


class SubAnimation(Animation):
    def __init__(
        self,
        animations: list[Animation],
        weights: list[float] = None,
        inverse: list[bool] = None,
    ) -> None:
        super().__init__()
        assert len(animations) > 0
        self.animations = deque(animations)
        self.sub_strips = []

        if weights is None:
            normalizer = len(animations)
            self.weights = [1.0 / normalizer for _ in animations]
        else:
            assert len(animations) == len(weights)
            normalizer = sum(weights)
            self.weights = [weight / normalizer for weight in weights]

        if inverse is None:
            self.inverse = [False] * len(animations)
        else:
            assert len(animations) == len(inverse)
            self.inverse = inverse

    def __repr__(self) -> str:
        return type(self).__name__ + f"({len(self.animations)}, {self.weights}, {self.inverse})"

    async def on_pause(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_pause(shared_data)

    async def on_resume(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_resume(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_track_change(shared_data)

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        for animation in self.animations:
            await animation.on_section(section, progress)

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_bar(bar, progress)

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_beat(beat, progress)

    async def on_tatum(self, tatum: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_tatum(tatum, progress)

    async def on_segment(self, segment: tk.model.Segment, progress: float) -> None:
        for animation in self.animations:
            await animation.on_segment(segment, progress)

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        weight_sum = [0]
        for weight in self.weights:
            weight_sum.append(weight_sum[-1] + weight)
        n = parent_strip.num_pixels()
        offsets = [round(ws * n) for ws in weight_sum]
        self.sub_strips = [
            SubStrip(
                strip=parent_strip,
                offset=offset,
                num_pixels=next_offset - offset,
                inverse=inverse,
            )
            for offset, next_offset, inverse in zip(offsets, offsets[1:], self.inverse)
        ]

    async def render(self, parent_strip: AbstractStrip) -> None:
        await super().render(parent_strip)
        for animation, sub_strip in zip(self.animations, self.sub_strips):
            await animation.render(sub_strip)

    @property
    def depends_on_spotify(self) -> bool:
        return any(animation.depends_on_spotify for animation in self.animations)

    def shift_forward(self, steps: int = 1) -> None:
        """Shift each animation substrip forward"""
        self.animations.rotate(steps)

    def shift_backward(self, steps: int = 1) -> None:
        """Shift each animation substrip backward"""
        self.animations.rotate(-steps)

    def mirror(self) -> None:
        """Mirror animations around the middle animation"""
        self.animations.reverse()
        for i in range(len(self.sub_strips) // 2):
            self.sub_strips[i].inverse ^= True
            self.sub_strips[-(i + 1)].inverse ^= True

    def invert(self) -> None:
        """Invert each animation"""
        for sub_strip in self.sub_strips:
            # invert SubStrip
            sub_strip.inverse ^= True
