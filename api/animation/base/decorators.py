from functools import wraps
from typing import Callable

import numpy as np

from ...color import Color
from .abstract import Animation


def on_change(function: Callable[..., np.ndarray]) -> Callable:
    @wraps(function)
    def wrapper(self: Animation, progress: float, xy: np.ndarray, **kwargs):
        if not np.array_equal(xy, getattr(self, "_xy", None)):
            setattr(self, "_xy", xy)
            self.change_callback(xy)
        return function(self, progress, xy, **kwargs)

    return wrapper


def save_previous(function: Callable[..., np.ndarray]) -> Callable:
    @wraps(function)
    def wrapper(self: Animation, progress: float, xy: np.ndarray, **kwargs):
        previous = getattr(self, "_prev", None)
        if previous is None or len(previous) != len(xy):
            previous = np.full(len(xy), Color())
        colors = function(self, progress, xy, previous=previous, **kwargs)
        setattr(self, "_prev", colors)
        return colors

    return wrapper
