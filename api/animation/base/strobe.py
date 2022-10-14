import time
from typing import Generator

from ...color import Color
from ...spotify.models import Section, Segment
from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip
from .absract import Animation
from .single_sub import SingleSubAnimation


class StrobeAnimation(SingleSubAnimation):
    def __init__(
        self,
        animation: Animation,
        duration_in_beats: int = 1,
        on_duration: float = 0.025,
        off_duration: float = 0.025,
        color: Color = Color(r=255, g=255, b=255),
    ) -> None:
        super().__init__(animation=animation)
        self.duration_in_beats = duration_in_beats
        self.on_duration = on_duration
        self.off_duration = off_duration
        self.color = color
        self.strobe_generator = None
        self.activate = False  # set to True to strobe
        self.bpm = 0.0

    async def on_pause(self, shared_data: SharedData) -> None:
        await super().on_pause(shared_data)
        self.bpm = 0

    async def on_resume(self, shared_data: SharedData) -> None:
        await super().on_resume(shared_data)
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    async def on_track_change(self, shared_data: SharedData) -> None:
        await super().on_track_change(shared_data)
        self.bpm = (await shared_data.get_audio_analysis()).tempo

    def strobe(self, strip: AbstractStrip) -> Generator[None, None, None]:
        start = time.time()
        duration = self.duration_in_beats * 60 / self.bpm
        while (time.time() - start) < duration:
            on = time.time()
            while (time.time() - on) < self.on_duration:
                strip.fill_color(self.color)
                yield
            off = time.time()
            while (time.time() - off) < self.off_duration:
                yield

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        self.strobe_generator = self.strobe(parent_strip)

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        if self.trigger_on_strip_change(parent_strip):
            self.on_strip_change(parent_strip)
        await super().render(parent_strip, progress)
        if self.activate and next(self.strobe_generator, True):
            self.strobe_generator = self.strobe(parent_strip)
            self.activate = False


class StrobeOnSectionAnimation(StrobeAnimation):
    async def on_section(self, section: Section, progress: float) -> None:
        self.activate = True
        return await super().on_section(section, progress)

    @property
    def depends_on_spotify(self) -> bool:
        return True


class StrobeOnLoudnessGradientAnimation(StrobeAnimation):
    async def on_segment(self, segment: Segment, progress: float) -> None:
        await super().on_segment(segment, progress)
        if segment.loudness_start_gradient_suppressed > 0.3:
            self.activate = True

    @property
    def depends_on_spotify(self) -> bool:
        return True
