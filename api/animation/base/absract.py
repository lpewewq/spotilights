from abc import ABC, abstractmethod

import numpy as np

from ...spotify.models import Bar, Beat, Section, Segment, Tatum
from ...spotify.shared_data import SharedData


class Animation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    async def on_pause(self, shared_data: SharedData) -> None:
        """Playback paused callback"""
        pass

    async def on_resume(self, shared_data: SharedData) -> None:
        """Playback resumed callback"""
        pass

    async def on_track_change(self, shared_data: SharedData) -> None:
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
        """Callback function used by @change_callback decorator when the xy coordinates change"""
        pass

    @abstractmethod
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        """Return rendered animation. For each xy coordinate return a Color"""

    @property
    @abstractmethod
    def depends_on_spotify(self) -> bool:
        """Property to identify spotify dependant animations"""
