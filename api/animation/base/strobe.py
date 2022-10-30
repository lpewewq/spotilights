import time
from abc import ABC
from typing import Generator

import numpy as np

from ...color import Color
from ...spotify.models import Segment
from ...spotify.shared_data import SharedData
from .sub import SingleSub


class Strobe(SingleSub, ABC):
    def __init__(self, config: "Strobe.Config") -> None:
        super().__init__(config)
        self.config: Strobe.Config
        self.strobe_generator = None
        self.activate = False  # set to True to strobe
        self.bpm = 0.0

    class Config(SingleSub.Config):
        duration_in_beats: int = 1
        on_duration: float = 0.025
        off_duration: float = 0.025
        color: Color = Color(r=255, g=255, b=255)

        @property
        def needs_spotify(self) -> bool:
            return True

    async def on_track_change(self, shared_data: SharedData) -> None:
        await super().on_track_change(shared_data)
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    def strobe(self, duration: float) -> Generator[bool, None, None]:
        start = time.time()
        while (time.time() - start) < duration:
            on = time.time()
            while (time.time() - on) < self.config.on_duration:
                yield True
            off = time.time()
            while (time.time() - off) < self.config.off_duration:
                yield False

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        if self.activate:
            if self.strobe_generator is None:
                self.strobe_generator = self.strobe(self.config.duration_in_beats * 60 / self.bpm)
            strobe = next(self.strobe_generator, None)
            if strobe is None:  # strobe finished
                self.strobe_generator = None
                self.activate = False
            elif strobe:
                return np.full(len(xy), self.config.color)
        return super().render(progress, xy)


class StrobeOnLoudnessGradient(Strobe):
    def on_segment(self, segment: Segment, progress: float) -> None:
        super().on_segment(segment, progress)
        if segment.loudness_start_gradient_suppressed > 0.3:
            self.activate = True
