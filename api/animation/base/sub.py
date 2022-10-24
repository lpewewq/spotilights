from abc import ABC
from collections import deque

import numpy as np
from pydantic import validator

from ...color import Color
from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData
from .abstract import Animation, AnimationModel
from .decorators import on_change


class SingleSub(Animation, ABC):
    def __init__(self, config: "Animation.Config" = None) -> None:
        super().__init__(config)
        self.config: SingleSub.Config
        self.animation = self.config.sub.construct()

    class Config(Animation.Config):
        sub: AnimationModel

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


class MultiSub(Animation):
    def __init__(self, config: "Animation.Config" = None) -> None:
        super().__init__(config)
        self.config: MultiSub.Config
        self.animations = deque([animation.construct() for animation in self.config.sub])

    class Config(Animation.Config):
        sub: list[AnimationModel]
        weights: list[float] = None

        @validator("weights", pre=True, always=True)
        def validate_weights(cls, v, values):
            sub = values.get("sub")
            if v is None:
                return [1.0 / len(sub)] * len(sub)
            if len(sub) != len(v):
                raise ValueError(f"Weights dimension mismatch {len(sub)} != {len(v)}.")
            normalizer = sum(v)
            return [weight / normalizer for weight in v]

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
        weight_sum = [0]
        for weight in self.config.weights:
            weight_sum.append(weight_sum[-1] + weight)
        offsets = [round(ws * n) for ws in weight_sum]
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


class MultiSubInvertable(MultiSub):
    def __init__(self, config: "MultiSub.Config" = None) -> None:
        from .inverse import Inverse

        # inject invert animation if needed
        config.sub = [
            sub
            if sub.animation is Inverse
            else AnimationModel(animation=Inverse, config=Inverse.Config(sub=sub, inverse=False))
            for sub in config.sub
        ]
        super().__init__(config)
        self.animations: list[Inverse]

    def reverse(self) -> None:
        super().reverse()
        # invert animations
        for i in range(len(self.animations) // 2):
            self.animations[i].config.inverse ^= True
            self.animations[-(i + 1)].config.inverse ^= True
