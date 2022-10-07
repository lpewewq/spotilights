import tekore as tk

from ...spotify.shared_data import SharedData
from ...strip.base import AbstractStrip, SubStrip
from .absract import Animation


class SubAnimation(Animation):
    def __init__(
        self,
        animations: list[Animation],
        weights: list[float] = None,
        inverse: list[bool] = None,
    ) -> None:
        super().__init__()
        assert len(animations) > 0
        self.animations = animations

        if weights is None:
            normalizer = len(animations)
            self.weights = [1.0 / normalizer for _ in animations]
        else:
            assert len(animations) == len(weights)
            normalizer = sum(weights)
            self.weights = [weight / normalizer for weight in weights]

        if inverse is None:
            self.inverse = [i % 2 == 1 for i in range(len(animations))]
        else:
            assert len(animations) == len(inverse)
            self.inverse = inverse

    def __repr__(self) -> str:
        return type(self).__name__ + f"({len(self.animations)})"

    def init_strip(self, strip: AbstractStrip) -> None:
        super().init_strip(strip)
        weight_sum = [0]
        for weight in self.weights:
            weight_sum.append(weight_sum[-1] + weight)
        n = strip.num_pixels()
        offsets = [round(ws * n) for ws in weight_sum]
        for animation, offset, next_offset, inverse in zip(self.animations, offsets, offsets[1:], self.inverse):
            animation.init_strip(
                SubStrip(
                    strip=strip,
                    offset=offset,
                    num_pixels=next_offset - offset,
                    inverse=inverse,
                )
            )

    async def on_pause(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_pause(shared_data)

    async def on_resume(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_resume(shared_data)

    async def on_track_change(self, shared_data: SharedData) -> None:
        for animation in self.animations:
            await animation.on_track_change(shared_data)

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        for animation in self.animations:
            await animation.on_section(section, progress)

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_bar(bar, progress)

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_beat(beat, progress)

    async def on_tatum(self, tatum: tk.model.TimeInterval, progress: float) -> None:
        for animation in self.animations:
            await animation.on_tatum(tatum, progress)

    async def on_segment(self, segment: tk.model.Segment, progress: float) -> None:
        for animation in self.animations:
            await animation.on_segment(segment, progress)

    async def on_loop(self) -> None:
        for animation in self.animations:
            await animation.on_loop()

    @property
    def depends_on_spotify(self) -> bool:
        return any(animation.depends_on_spotify for animation in self.animations)

    def shift_forward(self) -> None:
        """Shift each animation one substrip forward"""
        overflow_strip = self.animations[0].strip
        for left, right in zip(self.animations, self.animations[1:]):
            left.strip = right.strip
        self.animations[-1].strip = overflow_strip

    def shift_backward(self) -> None:
        """Shift each animation one substrip backward"""
        overflow_strip = self.animations[-1].strip
        for left, right in zip(self.animations[::-1][1:], self.animations[::-1]):
            right.strip = left.strip
        self.animations[0].strip = overflow_strip

    def mirror(self) -> None:
        """Mirror animations around the middle animation"""
        mid = len(self.animations) // 2
        for left, right in zip(self.animations[:mid], self.animations[::-1][:mid]):
            tmp = left.strip
            left.strip = right.strip
            right.strip = tmp

    def invert(self) -> None:
        """Invert each animation"""
        for animation in self.animations:
            # invert SubStrip
            animation.strip.inverse ^= True
