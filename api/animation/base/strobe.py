import time
from typing import Generator

import tekore as tk

from ...color import Color
from ...strip.base import AbstractStrip
from .absract import Animation
from .single_sub import SingleSubAnimation


class StrobeAnimation(SingleSubAnimation):
    def __init__(
        self,
        animation: Animation,
        n_strobes: int = 3,
        on_duration: float = 0.05,
        off_duration: float = 0.05,
        color: Color = Color(r=255, g=255, b=255),
    ) -> None:
        super().__init__(animation=animation)
        self.n_strobes = n_strobes
        self.on_duration = on_duration
        self.off_duration = off_duration
        self.color = color
        self.strobe_generator = None
        self.activate = False  # set to True to strobe

    def strobe(self, strip: AbstractStrip) -> Generator[None, None, None]:
        for _ in range(self.n_strobes):
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

    async def render(self, parent_strip: AbstractStrip) -> None:
        if self.trigger_on_strip_change(parent_strip):
            self.on_strip_change(parent_strip)
        await super().render(parent_strip)
        if self.activate and next(self.strobe_generator, True):
            self.strobe_generator = self.strobe(parent_strip)
            self.activate = False


class StrobeOnSectionAnimation(StrobeAnimation):
    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        self.activate = True
        return await super().on_section(section, progress)

    @property
    def depends_on_spotify(self) -> bool:
        return True
