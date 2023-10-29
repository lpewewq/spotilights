from abc import ABC, abstractmethod

import numpy as np
from pydantic import BaseModel, Extra, Field

from ..spotify.models import AudioAnalysis, Bar, Beat, Section, Segment, Tatum


class AbstractAnimation(BaseModel, ABC, extra=Extra.allow):
    """Interface for animations."""

    @property
    @abstractmethod
    def needs_spotify(self) -> bool:
        """Identify spotify dependant animations"""

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        """Track change callback"""
        pass

    def on_section(self, section: Section, progress: float) -> None:
        """Section callback"""
        pass

    def on_bar(self, bar: Bar, progress: float) -> None:
        """Bar callback"""
        pass

    def on_beat(self, beat: Beat, progress: float) -> None:
        """Beat callback"""
        pass

    def on_tatum(self, tatum: Tatum, progress: float) -> None:
        """Tatum callback"""
        pass

    def on_segment(self, segment: Segment, progress: float) -> None:
        """Segment callback"""
        pass

    def change_callback(self, xy: np.ndarray) -> None:
        """Callback function used by @on_change decorator when length of the xy coordinates change"""
        self.change_elements_callback(xy)

    def change_elements_callback(self, xy: np.ndarray) -> None:
        """Callback function used by @on_change decorator only when the xy coordinates change"""
        pass

    @abstractmethod
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        """Return rendered animation. For each xy coordinate return a Color"""


class SingleSub(AbstractAnimation, ABC):
    """Container for single animation."""

    animation: "Animation" = Field(...)

    @property
    def needs_spotify(self) -> bool:
        return self.animation.needs_spotify

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


class MultiSub(AbstractAnimation, ABC):
    """Container for multiple animations."""

    animations: list["Animation"] = Field(...)

    @property
    def needs_spotify(self) -> bool:
        return any(animation.needs_spotify for animation in self.animations)

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
