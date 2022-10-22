import numpy as np

from ...color import Color
from ...spotify.models.audio_analysis import Beat
from ..base.absract import Animation
from ..base.decorators import on_change
from ..base.inverse import Inverse
from .ease import ease_out_quint


class Slide(Inverse):
    def __init__(self, color: Color) -> None:
        super().__init__(_Slide(color, ease_out_quint), False)

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.inverse ^= True
        return super().on_beat(beat, progress)


class _Slide(Animation):
    def __init__(self, color: Color, ease_function) -> None:
        super().__init__()
        self.color = color
        self.ease_function = ease_function
        self.beat_start = 0
        self.beat_duration = 1

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.color})"

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.beat_start = beat.start
        self.beat_duration = beat.duration

    def change_callback(self, xy: np.ndarray) -> None:
        n = len(xy)
        colors = np.full(2 * n, Color(0, 0, 0))
        colors[(3 * n) // 4 : (3 * n) // 4 + n // 2] = np.full(n // 2, self.color)
        self.pattern = colors

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        beat_progress = min(1, (progress - self.beat_start) / self.beat_duration)
        beat_progress = self.ease_function(beat_progress)
        offset = (3 * n) // 4 - round(beat_progress * (n // 2))
        return self.pattern[offset : offset + n]

    def depends_on_spotify(self) -> bool:
        return True
