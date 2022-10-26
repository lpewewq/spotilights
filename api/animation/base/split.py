from collections import deque

import numpy as np
from pydantic import PositiveFloat, validator

from ...color import Color
from .abstract import Animation, AnimationModel
from .decorators import on_change
from .sub import MultiSub


class Split(MultiSub):
    def __init__(self, config: "Split.Config") -> None:
        super().__init__(config)
        self.config: Split.Config
        self.animations: deque[Animation] = deque(self.animations)

    class Config(MultiSub.Config):
        weights: list[PositiveFloat] = None

        @validator("weights", pre=True, always=True)
        def validate_weights(cls, v, values):
            subs = values.get("subs")
            if v is None:
                return [1.0 / len(subs)] * len(subs)
            if len(subs) != len(v):
                raise ValueError(f"Weights dimension mismatch {len(subs)} != {len(v)}.")
            normalizer = sum(v)
            if normalizer == 0:
                raise ValueError(f"Weights sum to 0.")
            return [weight / normalizer for weight in v]

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

    def shift_forward(self, steps: int = 1) -> None:
        """Shift each animation substrip forward"""
        self.animations.rotate(steps)

    def shift_backward(self, steps: int = 1) -> None:
        """Shift each animation substrip backward"""
        self.animations.rotate(-steps)

    def reverse(self) -> None:
        """Reverse animations"""
        self.animations.reverse()


class SplitInvertable(Split):
    def __init__(self, config: Split.Config) -> None:
        from .inverse import Inverse

        # inject invert animation if needed
        config.subs = [
            sub
            if sub.animation is Inverse
            else AnimationModel(animation=Inverse, config=Inverse.Config(sub=sub, inverse=False))
            for sub in config.subs
        ]
        super().__init__(config)
        self.animations: deque[Inverse]

    def reverse(self) -> None:
        super().reverse()
        # invert animations
        for i in range(len(self.animations) // 2):
            self.animations[i].config.inverse ^= True
            self.animations[-(i + 1)].config.inverse ^= True
