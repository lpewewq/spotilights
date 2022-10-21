import numpy as np

from ...color import Color
from ...spotify.models import Segment
from ..base import Animation


# Experimental
class Bar(Animation):
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)

    def __init__(self) -> None:
        super().__init__()
        self.loudness = lambda progress: 0

    def on_segment(self, segment: Segment, progress: float) -> None:
        super().on_segment(segment, progress)
        if segment.next:
            m1 = (segment.loudness_max - segment.loudness_start) / segment.loudness_max_time
            m2 = (segment.next.loudness_start - segment.loudness_max) / (segment.duration - segment.loudness_max_time)
            self.loudness = (
                lambda progress: m1 * (progress - segment.start) + segment.loudness_start
                if (progress <= segment.start + segment.loudness_max_time)
                else m2 * (progress - segment.start - segment.loudness_max_time) + segment.loudness_max
            )
        else:
            self.loudness = lambda progress: 0

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)
        colors = np.full(n, self.red)
        threshold = round(n * self.loudness(progress))
        colors[threshold:] = self.black
        return colors

    def depends_on_spotify(self) -> bool:
        return True
