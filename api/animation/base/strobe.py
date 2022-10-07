import time
from typing import Generator

import tekore as tk

from ...color import Color
from .absract import Animation
from .sub import SubAnimation


class StrobeAnimation(SubAnimation):
    def __init__(
        self,
        animation: Animation,
        n_strobes: int = 3,
        on_duration: float = 0.05,
        off_duration: float = 0.05,
        color: Color = Color(r=255, g=255, b=255),
    ) -> None:
        super().__init__(animations=[animation])
        self.n_strobes = n_strobes
        self.on_duration = on_duration
        self.off_duration = off_duration
        self.color = color
        self.strobe_generator = None
        self.activate = False  # set to True to strobe

    def strobe(self) -> Generator[None, None, None]:
        for _ in range(self.n_strobes):
            on = time.time()
            while (time.time() - on) < self.on_duration:
                self.strip.fill_color(self.color)
                yield
            off = time.time()
            while (time.time() - off) < self.off_duration:
                yield

    async def on_loop(self) -> None:
        await super().on_loop()
        if self.activate:
            if self.strobe_generator is None:
                self.strobe_generator = self.strobe()
            if next(self.strobe_generator, True):
                self.strobe_generator = None
                self.activate = False


class StrobeOnSectionAnimation(StrobeAnimation):
    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        self.activate = True
        return await super().on_section(section, progress)

    @property
    def depends_on_spotify(self) -> bool:
        return True
