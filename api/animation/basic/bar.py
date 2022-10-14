from ...color import Color
from ...spotify.models import Segment
from ...strip.base import AbstractStrip
from ..base import Animation


class BarAnimation(Animation):
    def __init__(self) -> None:
        super().__init__()
        self.loudness = lambda progress: 0

    async def on_segment(self, segment: Segment, progress: float) -> None:
        await super().on_segment(segment, progress)
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

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        await super().render(parent_strip, progress)
        n = parent_strip.num_pixels()
        l = self.loudness(progress)
        t = round(n * l)
        for i in range(n):
            if i < t:
                parent_strip.set_pixel_color(i, Color(255, 0, 0))
            else:
                parent_strip.set_pixel_color(i, Color(0, 0, 0))

    def depends_on_spotify(self) -> bool:
        return True
