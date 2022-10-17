import time
from typing import Generator

import numpy as np

from ...color import Color
from ...spotify.models import Segment
from ...spotify.shared_data import SharedData
from .absract import Animation
from .sub import SingleSubAnimation


class StrobeAnimation(SingleSubAnimation):
    def __init__(
        self,
        animation: Animation,
        duration_in_beats: int = 1,
        on_duration: float = 0.025,
        off_duration: float = 0.025,
        color: Color = Color(r=255, g=255, b=255),
    ) -> None:
        super().__init__(animation=animation)
        self.duration_in_beats = duration_in_beats
        self.on_duration = on_duration
        self.off_duration = off_duration
        self.color = color
        self.strobe_generator = None
        self.activate = False  # set to True to strobe
        self.bpm = 0.0

    async def on_pause(self, shared_data: SharedData) -> None:
        await super().on_pause(shared_data)
        self.bpm = 0

    async def on_resume(self, shared_data: SharedData) -> None:
        await super().on_resume(shared_data)
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    async def on_track_change(self, shared_data: SharedData) -> None:
        await super().on_track_change(shared_data)
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    def strobe(self, duration: float) -> Generator[bool, None, None]:
        start = time.time()
        while (time.time() - start) < duration:
            on = time.time()
            while (time.time() - on) < self.on_duration:
                yield True
            off = time.time()
            while (time.time() - off) < self.off_duration:
                yield False

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        if self.activate:
            if self.strobe_generator is None:
                self.strobe_generator = self.strobe(self.duration_in_beats * 60 / self.bpm)
            strobe = next(self.strobe_generator, None)
            if strobe is None:  # strobe finished
                self.strobe_generator = None
                self.activate = False
            elif strobe:
                return np.full(len(xy), self.color)
        return super().render(progress, xy)


class StrobeOnLoudnessGradientAnimation(StrobeAnimation):
    def on_segment(self, segment: Segment, progress: float) -> None:
        super().on_segment(segment, progress)
        if segment.loudness_start_gradient_suppressed > 0.3:
            self.activate = True

    @property
    def depends_on_spotify(self) -> bool:
        return True
