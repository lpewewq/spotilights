from abc import ABC
from collections import deque

import numpy as np

from ...color import Color
from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData
from .absract import Animation
from .decorators import on_change


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

    def on_section(self, section: Section, progress: float) -> None:
        self.animation.on_section(section, progress)

    def on_bar(self, bar: Bar, progress: float) -> None:
        self.animation.on_bar(bar, progress)

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.animation.on_beat(beat, progress)

    def on_tatum(self, tatum: Tatum, progress: float) -> None:
        self.animation.on_tatum(tatum, progress)

    def on_segment(self, segment: Segment, progress: float) -> None:
        self.animation.on_segment(segment, progress)

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        return self.animation.render(progress, xy)

    @property
    def depends_on_spotify(self) -> bool:
        return self.animation.depends_on_spotify


class MultiSubAnimation(Animation):
    def __init__(
        self,
        animations: list[Animation],
        weights: list[float] = None,
    ) -> None:
        super().__init__()
        assert len(animations) > 0
        self.animations = deque(animations)

        if weights is None:
            normalizer = len(animations)
            weights = [1.0 / normalizer for _ in animations]
        else:
            assert len(animations) == len(weights)
            normalizer = sum(weights)
            weights = [weight / normalizer for weight in weights]

        self.weight_sum = [0]
        for weight in weights:
            self.weight_sum.append(self.weight_sum[-1] + weight)

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

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        offsets = [round(ws * n) for ws in self.weight_sum]
        self.offsets = list(zip(offsets, offsets[1:]))

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        colors = np.empty(len(xy), dtype=Color)
        for animation, (offset, next_offset) in zip(self.animations, self.offsets):
            colors[offset:next_offset] = animation.render(progress, xy[offset:next_offset])
        return colors

    @property
    def depends_on_spotify(self) -> bool:
        return any(animation.depends_on_spotify for animation in self.animations)

    def shift_forward(self, steps: int = 1) -> None:
        """Shift each animation substrip forward"""
        self.animations.rotate(steps)

    def shift_backward(self, steps: int = 1) -> None:
        """Shift each animation substrip backward"""
        self.animations.rotate(-steps)

    def reverse(self) -> None:
        """Reverse animations"""
        self.animations.reverse()


class InvertableMultiSubAnimation(MultiSubAnimation):
    def __init__(self, animations: list[Animation], weights: list[float] = None, inverse: list[bool] = None) -> None:
        from .inverse import InverseAnimation

        if inverse is None:
            self.inverse = [i % 2 == 1 for i in range(len(animations))]
        else:
            assert len(animations) == len(inverse)
            self.inverse = inverse
        animations = [InverseAnimation(a, inv) for a, inv in zip(animations, self.inverse)]
        super().__init__(animations, weights)

    def reverse(self) -> None:
        super().reverse()
        # invert animations
        for i in range(len(self.animations) // 2):
            self.animations[i].inverse ^= True
            self.animations[-(i + 1)].inverse ^= True
