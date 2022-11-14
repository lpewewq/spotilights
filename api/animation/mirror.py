from typing import Literal

import numpy as np
from pydantic import conlist

from ..color import Color
from .abstract import SingleSub
from .utils.decorators import on_change


class Mirror(SingleSub):
    """Container mirroring a single animation."""

    name: Literal["Mirror"]
    inverse: conlist(bool, min_items=2) = [False, True]

    def change_callback(self, xy: np.ndarray) -> None:
        self.chunk_size, self.n_large_chunks = divmod(len(xy), len(self.inverse))
        if self.n_large_chunks > 0:
            self.chunk_size += 1
        else:
            self.n_large_chunks = len(self.inverse)

    @on_change
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        sub_colors = super().render(progress, xy[: self.chunk_size])
        colors = np.empty(len(xy), dtype=Color)

        # fill colors with chunks of sub_colors
        offset = 0
        for i, inverse in enumerate(self.inverse):
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
