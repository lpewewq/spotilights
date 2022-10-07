from abc import ABC, abstractmethod

import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip


class Animation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    def __init__(self) -> None:
        self.strip: AbstractStrip = None

    def init_strip(self, strip: AbstractStrip) -> None:
        """
        Top down initialization of the LED strip.
        Must be called before the animation loop starts
        """
        self.strip = strip

    async def on_pause(self, shared_data: SharedData) -> None:
        """Playback paused callback"""
        pass

    async def on_resume(self, shared_data: SharedData) -> None:
        """Playback resumed callback"""
        pass

    async def on_track_change(self, shared_data: SharedData) -> None:
        """Track change callback"""
        pass

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        """Section callback"""
        pass

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        """Bar callback"""
        pass

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        """Beat callback"""
        pass

    async def on_tatum(self, tatum: tk.model.TimeInterval, progress: float) -> None:
        """Tatum callback"""
        pass

    async def on_segment(self, segment: tk.model.Segment, progress: float) -> None:
        """Segment callback"""
        pass

    async def on_loop(self) -> None:
        """Animation loop"""
        pass

    @property
    @abstractmethod
    def depends_on_spotify(self) -> bool:
        """Property to identify spotify dependant animations"""
