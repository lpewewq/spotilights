import numpy as np

from ...color import Color
from .absract import Animation
from .decorators import on_change
from .sub import SingleSubAnimation


class MirrorAnimation(SingleSubAnimation):
    def __init__(self, animation: Animation, divisions: int = 2, inverse: list[bool] = None) -> None:
        super().__init__(animation=animation)
        assert divisions > 0
        self.divisions = divisions
        if inverse is None:
            self.inverse = [i % 2 == 1 for i in range(divisions)]
        else:
            assert len(inverse) == divisions
            self.inverse = inverse

    def change_callback(self, xy: np.ndarray) -> None:
        self.chunk_size, self.n_large_chunks = divmod(len(xy), self.divisions)
        if self.n_large_chunks > 0:
            self.chunk_size += 1
        else:
            self.n_large_chunks = self.divisions

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        sub_colors = super().render(progress, xy[: self.chunk_size])
        colors = np.empty(len(xy), dtype=Color)

        # fill colors with chunks of sub_colors
        offset = 0
        for i, inverse in zip(range(self.divisions), self.inverse):
            if i < self.n_large_chunks:
                chunk = sub_colors
            else:
                chunk = sub_colors[:-1]
            if inverse:
                chunk = chunk[::-1]
            chunk_length = len(chunk)
            colors[offset : offset + chunk_length] = chunk
            offset += chunk_length

        return colors
