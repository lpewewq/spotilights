import numpy as np
from pydantic import PyObject

from ...color import Color
from ...spotify.models.audio_analysis import Beat
from ..base.abstract import Animation
from ..base.decorators import on_change
from .ease import ease_out_quint


class Slide(Animation):
    def __init__(self, config: "Slide.Config") -> None:
        super().__init__(config)
        self.config: Slide.Config
        self.beat_start = 0
        self.beat_duration = 1

    class Config(Animation.Config):
        color: Color = Color(r=255)

        @property
        def needs_spotify(self) -> bool:
            return True

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.beat_start = beat.start
        self.beat_duration = beat.duration

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        colors = np.full(2 * n, Color(0, 0, 0))
        colors[(3 * n) // 4 : (3 * n) // 4 + n // 2] = np.full(n // 2, self.config.color)
        self.pattern = colors

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat_progress = min(1, (progress - self.beat_start) / self.beat_duration)
        beat_progress = ease_out_quint(beat_progress)
        offset = (3 * n) // 4 - round(beat_progress * (n // 2))
        return self.pattern[offset : offset + n]
