from functools import wraps
from typing import Callable

import numpy as np

from ...color import Color
from ..abstract import AbstractAnimation


def on_change(function: Callable[..., np.ndarray]) -> Callable:
    @wraps(function)
    def wrapper(self: AbstractAnimation, progress: float, xy: np.ndarray, **kwargs):
        _xy = getattr(self, "_xy", None)
        if _xy is None:
            self.change_callback(xy)
        elif len(xy) != len(_xy):
            self.change_callback(xy)
        elif not np.array_equal(xy, _xy):
            self.change_elements_callback(xy)
        setattr(self, "_xy", xy)
        return function(self, progress, xy, **kwargs)

    return wrapper


def save_previous(function: Callable[..., np.ndarray]) -> Callable:
    @wraps(function)
    def wrapper(self: AbstractAnimation, progress: float, xy: np.ndarray, **kwargs):
        previous = getattr(self, "_prev", None)
        if previous is None or len(previous) != len(xy):
            previous = np.full(len(xy), Color())
        colors = function(self, progress, xy, previous=previous, **kwargs)
        setattr(self, "_prev", colors)
        return colors

    return wrapper
