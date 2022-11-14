import time
from abc import ABC
from typing import Generator, Literal

import numpy as np
from pydantic import Field, confloat

from ..color import Color
from ..spotify.models import AudioAnalysis, Segment
from .abstract import SingleSub


class Strobe(SingleSub, ABC):
    duration_in_beats: confloat(ge=0, le=4, multiple_of=0.5) = Field(
        1.0, config_type="Numerical", title="Duration in Beats", description=" "
    )
    on_duration: confloat(ge=0.015, le=0.15, multiple_of=0.015) = Field(
        0.03, config_type="Numerical", title="On Duration", description="s"
    )
    off_duration: confloat(ge=0.015, le=0.15, multiple_of=0.015) = Field(
        0.03, config_type="Numerical", title="Off Duration", description="s"
    )
    color: Color = Field(Color(r=255, g=255, b=255), config_type="Color", title="Strobe Color")

    _strobe_generator = None
    _activate = False  # set to True to strobe
    _bpm = 1

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self._bpm = analysis.tempo
        return super().on_track_change(analysis)

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
        if self._activate:
            if self._strobe_generator is None:
                self._strobe_generator = self.strobe(self.duration_in_beats * 60 / self._bpm)
            strobe = next(self._strobe_generator, None)
            if strobe is None:  # strobe finished
                self._strobe_generator = None
                self._activate = False
            elif strobe:
                return np.full(len(xy), self.color)
        return super().render(progress, xy)


class StrobeOnLoudnessGradient(Strobe):
    """Container animation which strobes on high loudness gradients."""

    name: Literal["StrobeOnLoudnessGradient"]
    threshold: confloat(ge=0.0, le=1.0, multiple_of=0.05) = Field(
        0.3, config_type="Numerical", title="Strobe Threshold", description=" "
    )

    def on_segment(self, segment: Segment, progress: float) -> None:
        if segment.loudness_start_gradient_suppressed > self.threshold:
            self._activate = True
        return super().on_segment(segment, progress)
