from abc import ABC

import numpy as np
from pydantic import conlist

from ...spotify.models import AudioAnalysis, Bar, Beat, Section, Segment, Tatum
from .abstract import Animation, AnimationModel


class SingleSub(Animation, ABC):
    def __init__(self, config: "SingleSub.Config") -> None:
        super().__init__(config)
        self.config: SingleSub.Config
        self.animation: Animation = self.config.sub.construct()

    class Config(Animation.Config):
        sub: AnimationModel

        @property
        def needs_spotify(self) -> bool:
            return self.sub.config.needs_spotify

        def schema(self, *args, **kwargs):
            schema = super().schema(*args, **kwargs)
            schema["sub"] = self.sub.schema(*args, **kwargs)
            return schema

    def update_config(self, config: "SingleSub.Config"):
        if isinstance(self.animation, config.sub.animation):
            self.animation.update_config(config.sub.config)
        else:
            self.animation = config.sub.construct()
        super().update_config(config)

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self.animation.on_track_change(analysis)

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


class MultiSub(Animation, ABC):
    def __init__(self, config: "MultiSub.Config") -> None:
        super().__init__(config)
        self.config: MultiSub.Config
        self.animations: list[Animation] = [animation.construct() for animation in self.config.subs]

    class Config(Animation.Config):
        subs: conlist(AnimationModel, min_items=1)

        @property
        def needs_spotify(self) -> bool:
            return any(sub.config.needs_spotify for sub in self.subs)

        def schema(self, *args, **kwargs):
            schema = super().schema(*args, **kwargs)
            schema["subs"] = [sub.schema(*args, **kwargs) for sub in self.subs]
            return schema

    def update_config(self, config: "MultiSub.Config"):
        animations = []
        for i, sub in enumerate(config.subs):
            if i < len(self.animations) and isinstance(self.animations[i], sub.animation):
                self.animations[i].update_config(sub.config)
                animations.append(self.animations[i])
            else:
                animations.append(sub.construct())
        self.animations = animations
        super().update_config(config)

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        for animation in self.animations:
            animation.on_track_change(analysis)

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
