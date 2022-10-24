import numpy as np
from pydantic import conlist

from ...color import Color
from .abstract import Animation
from .decorators import on_change
from .sub import SingleSub


class Mirror(SingleSub):
    def __init__(self, config: "Mirror.Config") -> None:
        super().__init__(config)
        self.config: Mirror.Config

    class Config(SingleSub.Config):
        inverse: conlist(bool, min_items=2) = [False, True]

        @property
        def divisions(self):
            return len(self.inverse)

    def change_callback(self, xy: np.ndarray) -> None:
        self.chunk_size, self.n_large_chunks = divmod(len(xy), self.config.divisions)
        if self.n_large_chunks > 0:
            self.chunk_size += 1
        else:
            self.n_large_chunks = self.config.divisions

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        sub_colors = super().render(progress, xy[: self.chunk_size])
        colors = np.empty(len(xy), dtype=Color)

        # fill colors with chunks of sub_colors
        offset = 0
        for i, inverse in enumerate(self.config.inverse):
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
