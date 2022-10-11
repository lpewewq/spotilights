from ...strip.base import AbstractStrip, SubStrip
from .absract import Animation
from .single_sub import SingleSubAnimation


class InverseAnimation(SingleSubAnimation):
    def __init__(self, animation: Animation) -> None:
        super().__init__(animation=animation)
        self._inverted_strip = None

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        self._inverted_strip = SubStrip(strip=parent_strip, inverse=True)

    async def render(self, parent_strip: AbstractStrip, progress: float) -> None:
        if self.trigger_on_strip_change(parent_strip):
            self.on_strip_change(parent_strip)
        await super().render(self._inverted_strip, progress)
