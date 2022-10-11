import time
from abc import ABC, abstractclassmethod
from typing import Generator

from ...color import Color
from ...strip.base import AbstractStrip
from .absract import Animation


class BaseIteratorAnimation(Animation, ABC):
    def __init__(self, delay: float) -> None:
        super().__init__()
        self.delay = delay
        self.rainbow = [self.wheel(pos) for pos in range(256)]
        self._generator = None

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

    @abstractclassmethod
    def generator(self, strip: AbstractStrip) -> Generator[float, None, None]:
        """Animation generator"""

    def _infinite_generator(self, strip: AbstractStrip) -> Generator[None, None, None]:
        while True:
            try:
                for delay in self.generator(strip):
                    t = time.time()
                    yield
                    if delay:
                        while (time.time() - t) < delay:
                            yield
            except StopIteration:
                yield

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        self._generator = self._infinite_generator(parent_strip)

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        await super().render(parent_strip, progress)
        next(self._generator)
