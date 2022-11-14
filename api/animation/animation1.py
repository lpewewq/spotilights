import random
import time
from typing import Literal

import numpy as np

from ..color import Color
from ..spotify.models import Bar, Beat, Section
from .abstract import AbstractAnimation


class Animation1(AbstractAnimation):
    """TODO"""

    name: Literal["Animation1"]
    col_a = Color(r=255, g=0, b=0)
    col_b = Color(r=0, g=255, b=0)
    col_c = Color(r=0, g=0, b=255)
    col_d = Color(r=0, g=0, b=0)

    _last_update = time.time()
    _wave_pos = 0
    _wave_vel = 0.01
    _beat_num = 0
    _bar_num = 0
    _bar_start = 0
    _bar_duration = 1
    _beat_pair_progress = 0
    _beat_pair_duration = 1

    @property
    def needs_spotify(self) -> bool:
        return True

    def get_bell(self, x):
        return 1 / (1 + x**2) ** 1.5

    def swap_cols(self):
        col_tmp = self.col_a
        self.col_a = self.col_b
        self.col_b = col_tmp
        col_tmp = self.col_c
        self.col_c = self.col_d
        self.col_d = col_tmp

    def on_section(self, section: Section, progress: float) -> None:
        self._wave_vel = section.tempo / 6000
        self._wave_pos = 0
        self._bar_num = 0

        # Change colors
        choice = random.randint(0, 3)
        if choice == 0:
            self.col_c = Color(r=255, g=0, b=0)
            self.col_d = Color(r=0, g=255, b=0)
        if choice == 1:
            self.col_c = Color(r=255, g=0, b=0)
            self.col_d = Color(r=0, g=0, b=255)
        if choice == 2:
            self.col_c = Color(r=26, g=0, b=0)
            self.col_d = Color(r=0, g=0, b=255)
        if choice == 3:
            self.col_c = Color(r=255, g=0, b=0)
            self.col_d = Color(r=255, g=255, b=0)

    def on_bar(self, bar: Bar, progress: float) -> None:
        self._bar_num += 1
        self._bar_start = bar.start
        self._bar_duration = bar.duration

    def on_beat(self, beat: Beat, progress: float) -> None:
        self._beat_num += 1
        self.swap_cols()

        if self._beat_num % 2 == 1:
            self._beat_pair_progress = 0
            self._beat_pair_duration = beat.duration * 2

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)

        now = time.time()
        delta = now - self._last_update
        self._last_update = now
        self._beat_pair_progress += delta

        if self._bar_num == 0:
            c_a = self.col_a
            c_b = self.col_b
        if self._bar_num == 1:
            bar_progress = (progress - self._bar_start) / self._bar_duration
            c_a = Color.lerp(self.col_a, self.col_c, bar_progress)
            c_b = Color.lerp(self.col_b, self.col_d, bar_progress)
        if self._bar_num > 1:
            self.col_a = self.col_c
            self.col_b = self.col_d
            c_a = self.col_a
            c_b = self.col_b

        beat_pair_proc = self._beat_pair_progress / self._beat_pair_duration

        if self._beat_num % 32 < 24:
            if self._bar_num % 6 < 3:
                cycle_proc = beat_pair_proc
            else:
                cycle_proc = 1 - beat_pair_proc
        else:
            cycle_proc = (self._beat_num % 8) / 8

        i = np.arange(-n, 0)
        scaling1 = 1 / ((1 + ((i + cycle_proc * n) / 10) ** 2) ** 1.5)
        scaling2 = 1 / ((1 + ((i + (cycle_proc + 1) * n) / 10) ** 2) ** 1.5)
        scalings = np.full(len(xy), 0.1) + (scaling1 + scaling2)

        ii = np.linspace(-np.pi, np.pi, num=n) + self._wave_pos
        col1 = np.abs(np.sin(ii)) * c_a
        col2 = np.abs(np.cos(ii)) * c_b
        colors = (col1 + col2) * scalings
        return colors
