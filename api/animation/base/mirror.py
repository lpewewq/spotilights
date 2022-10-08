from ...strip.base import AbstractStrip, MirroredStrip
from .absract import Animation
from .single_sub import SingleSubAnimation


class MirrorAnimation(SingleSubAnimation):
    def __init__(self, animation: Animation, divisions: int = 2, inverse: list[bool] = None) -> None:
        super().__init__(animation=animation)
        self.divisions = divisions
        self.inverse = inverse
        self._mirrored_strip = None

    def on_strip_change(self, parent_strip: AbstractStrip) -> None:
        super().on_strip_change(parent_strip)
        self._mirrored_strip = MirroredStrip(strip=parent_strip, divisions=self.divisions, inverse=self.inverse)

    async def render(self, parent_strip: AbstractStrip) -> None:
        if self.trigger_on_strip_change(parent_strip):
            self.on_strip_change(parent_strip)
        await super().render(self._mirrored_strip)
