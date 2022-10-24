import random
import time

import numpy as np

from ...color import Color
from ...spotify.models import Bar, Beat, Section
from ..base import Animation


class Animation1(Animation):
    def __init__(self, config: "Animation.Config") -> None:
        super().__init__(config)
        self.last_update = time.time()
        # Wave
        self.col_a = Color(r=255, g=0, b=0)
        self.col_b = Color(r=0, g=255, b=0)
        self.col_c = Color(r=0, g=0, b=255)
        self.col_d = Color(r=0, g=0, b=0)
        self.wave_pos = 0
        self.wave_vel = 0.01

        self.beat_num = 0
        self.bar_num = 0
        self.bar_start = 0
        self.bar_duration = 1
        self.beat_pair_progress = 0
        self.beat_pair_duration = 1

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
        self.wave_vel = section.tempo / 6000
        self.wave_pos = 0
        self.bar_num = 0

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
        self.bar_num += 1
        self.bar_start = bar.start
        self.bar_duration = bar.duration

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.beat_num += 1
        self.swap_cols()

        if self.beat_num % 2 == 1:
            self.beat_pair_progress = 0
            self.beat_pair_duration = beat.duration * 2

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        n = len(xy)

        now = time.time()
        delta = now - self.last_update
        self.last_update = now
        self.beat_pair_progress += delta

        if self.bar_num == 0:
            c_a = self.col_a
            c_b = self.col_b
        if self.bar_num == 1:
            bar_progress = (progress - self.bar_start) / self.bar_duration
            c_a = Color.lerp(self.col_a, self.col_c, bar_progress)
            c_b = Color.lerp(self.col_b, self.col_d, bar_progress)
        if self.bar_num > 1:
            self.col_a = self.col_c
            self.col_b = self.col_d
            c_a = self.col_a
            c_b = self.col_b

        beat_pair_proc = self.beat_pair_progress / self.beat_pair_duration

        if self.beat_num % 32 < 24:
            if self.bar_num % 6 < 3:
                cycle_proc = beat_pair_proc
            else:
                cycle_proc = 1 - beat_pair_proc
        else:
            cycle_proc = (self.beat_num % 8) / 8

        i = np.arange(-n, 0)
        scaling1 = 1 / ((1 + ((i + cycle_proc * n) / 10) ** 2) ** 1.5)
        scaling2 = 1 / ((1 + ((i + (cycle_proc + 1) * n) / 10) ** 2) ** 1.5)
        scalings = np.full(len(xy), 0.1) + (scaling1 + scaling2)

        ii = np.linspace(-np.pi, np.pi, num=n) + self.wave_pos
        col1 = np.abs(np.sin(ii)) * c_a
        col2 = np.abs(np.cos(ii)) * c_b
        colors = (col1 + col2) * scalings
        return colors

    @property
    def depends_on_spotify(self) -> bool:
        return True
