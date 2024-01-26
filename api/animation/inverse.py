from typing import Literal

import numpy as np
from pydantic import Field

from ..spotify.models.audio_analysis import Bar, Beat, Section, Segment, Tatum
from .abstract import SingleSub


class Inverse(SingleSub):
    """Container inverting an animation."""

    name: Literal["Inverse"]
    _inverse: bool = True

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        if self._inverse:
            return super().render(progress, xy[::-1])[::-1]
        else:
            return super().render(progress, xy)


class InverseOnEvent(Inverse):
    """Container inverting the animation on specific events."""

    _inverse: bool = False

    class Config:
        title = "Inverse"

    name: Literal["InverseOnEvent"]
    invert_on_section: bool = Field(False, description="Invert on section")
    invert_on_bar: bool = Field(False, description="Invert on bar")
    invert_on_beat: bool = Field(False, description="Invert on beat")
    invert_on_tatum: bool = Field(False, description="Invert on tatum")
    invert_on_segment: bool = Field(False, description="Invert on segment")

    @property
    def needs_spotify(self) -> bool:
        return True

    def on_section(self, section: Section, progress: float) -> None:
        self._inverse ^= self.invert_on_section
        return super().on_section(section, progress)

    def on_bar(self, bar: Bar, progress: float) -> None:
        self._inverse ^= self.invert_on_bar
        return super().on_bar(bar, progress)

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._inverse ^= self.invert_on_beat
        return super().on_beat(beat, progress)

    def on_tatum(self, tatum: Tatum, progress: float) -> None:
        self._inverse ^= self.invert_on_tatum
        return super().on_tatum(tatum, progress)

    def on_segment(self, segment: Segment, progress: float) -> None:
        self._inverse ^= self.invert_on_segment
        return super().on_segment(segment, progress)
