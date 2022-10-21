import time
from abc import ABC, abstractclassmethod
from typing import Generator, Union

import numpy as np

from .absract import Animation
from .decorators import on_change, save_previous


class BaseIterator(Animation, ABC):
    @abstractclassmethod
    def generator(self, xy: np.ndarray) -> Generator[tuple[np.ndarray, float], None, None]:
        """Animation generator"""

    def infinite_generator(self, xy: np.ndarray) -> Generator[Union[np.ndarray, None], None, None]:
        while True:
            try:
                for generated, delay in self.generator(xy):
                    t = time.time()
                    yield generated
                    while (time.time() - t) < delay:
                        yield
            except StopIteration:
                yield

    def change_callback(self, xy: np.ndarray) -> None:
        self._generator = self.infinite_generator(xy)

    @on_change
    @save_previous
    def render(self, progress: float, xy: np.ndarray, previous: np.ndarray) -> np.ndarray:
        generated = next(self._generator)
        if generated is None:
            return previous
        else:
            return generated
