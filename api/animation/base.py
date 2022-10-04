from abc import ABC

import tekore as tk

from ..color import Color
from ..spotify.shared_data import SharedData
from ..strip.base import LEDStrip


class BaseAnimation(ABC):
    """Interface for animations."""

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    def __init__(self, strip: LEDStrip, shared_data: SharedData) -> None:
        self.strip: LEDStrip = strip
        self.shared_data: SharedData = shared_data

    async def on_loop(self) -> None:
        """Animation loop"""
        pass

    async def on_pause(self) -> None:
        """Playback paused callback"""
        pass

    async def on_resume(self) -> None:
        """Playback resumed callback"""
        pass

    async def on_track_change(self) -> None:
        """Track change callback"""
        pass

    async def on_section(self, section: tk.model.TimeInterval) -> None:
        """Section callback"""
        pass

    async def on_beat(self, beat: tk.model.TimeInterval) -> None:
        """Beat callback"""
        pass


class BaseRainbowAnimation(BaseAnimation, ABC):
    def __init__(self, delay: float,  *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.delay = delay
        self.rainbow = [self.wheel(pos) for pos in range(256)]

    def wheel(self, pos: int) -> Color:
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(r=pos * 3, g=255 - pos * 3, b=0)
        elif pos < 170:
            pos -= 85
            return Color(r=255 - pos * 3, g=0, b=pos * 3)
        else:
            pos -= 170
            return Color(r=0, g=pos * 3, b=255 - pos * 3)
