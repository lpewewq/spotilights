import time

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

        self.on_time = 0
        self.off_time = 0
        self.i_strobes = 0
        self.toggle = True
        self.activate = False  # set to True to strobe

    def strobe(self):
        if self.toggle:
            if (time.time() - self.off_time) < self.off_duration:
                return
            self.on_time = time.time()

            self.strip.fill_color(self.color)
            self.toggle = not self.toggle
        else:
            if (time.time() - self.on_time) < self.on_duration:
                return
            self.off_time = time.time()

            self.toggle = not self.toggle
            self.i_strobes = (self.i_strobes + 1) % self.n_strobes
            if self.i_strobes == 0:
                self.activate = False

    async def on_loop(self) -> None:
        await super().on_loop()
        if self.activate:
            self.strobe()


class StrobeOnSectionAnimation(StrobeAnimation):
    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        self.activate = True
        return await super().on_section(section, progress)

    @property
    def depends_on_spotify(self) -> bool:
        return True
