import math
import random
import time

import tekore as tk

from ...color import Color
from ...strip.base.sub import AbstractStrip
from ..base import Animation


class PhilippAnimation(Animation):
    def __init__(self) -> None:
        super().__init__()
        self.last_update = time.time()
        # Wave
        self.col_a = Color(r=255, g=0, b=0)
        self.col_b = Color(r=0, g=255, b=0)
        self.col_c = Color(r=0, g=0, b=255)
        self.col_d = Color(r=0, g=0, b=0)
        self.brightness = None
        self.wave_pos = 0
        self.wave_vel = 1
        self.wave_freq = 1

        # state
        self.time = 0
        self.section_num = 0
        self.section_bars = 0
        self.bar_num = 0
        self.bar_progress = 0
        self.bar_duration = 1
        self.beat_num = 0
        self.beat_progress = 0
        self.beat_duration = 1
        self.beat_pair_progress = 0
        self.beat_pair_duration = 1

    def init_strip(self, strip: AbstractStrip) -> None:
        super().init_strip(strip)
        self.center = self.strip.num_pixels() / 2
        self.brightness = [1.0] * self.strip.num_pixels()

    def get_bell(self, x):
        return 1 / pow(1 + pow(x, 2), 3 / 2)

    def swap_cols(self):
        col_tmp = self.col_a
        self.col_a = self.col_b
        self.col_b = col_tmp
        col_tmp = self.col_c
        self.col_c = self.col_d
        self.col_d = col_tmp

    async def on_section(self, section: tk.model.Section, progress: float) -> None:
        if section is None:
            return
        self.sectionLoudness = section.loudness
        self.wave_vel = section.tempo / 100
        self.wave_freq = 1

        # Center color again
        self.wave_pos = 0
        self.wave_freq = 1

        # Start with first bar
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
        self.wave_pos = 0

        self.section_num += 1

    async def on_bar(self, bar: tk.model.TimeInterval, progress: float) -> None:
        if bar is None:
            return
        self.bar_num += 1
        self.bar_duration = bar.duration
        self.bar_progress = progress

    async def on_beat(self, beat: tk.model.TimeInterval, progress: float) -> None:
        if beat is None:
            return
        self.beat_num += 1
        self.beat_duration = beat.duration
        self.beat_progress = progress

        self.swap_cols()

        if self.section_num % 4 != 3 and self.beat_num % 2 == 1:
            self.brightness = [1.0] * self.strip.num_pixels()
            self.beat_pair_progress = 0
            self.beat_pair_duration = self.beat_duration * 2

        if self.section_num % 4 == 3:
            for i in range(0, self.strip.num_pixels()):
                self.brightness[i] += self.get_bell((i - ((self.beat_num % 5) / 4) * 287) / 10)

    async def on_loop(self) -> None:
        now = time.time()
        delta = now - self.last_update
        self.last_update = now

        self.time += delta
        self.beat_progress += delta
        self.beat_pair_progress += delta
        self.bar_progress += delta

        # Lerp colors in first bar of section (todo: lerp in HSV, not in RGB)
        if self.bar_num == 0:
            c_a = self.col_a.blend(self.col_c, 0)
            c_b = self.col_b.blend(self.col_d, 0)
        if self.bar_num == 1:
            c_a = self.col_a.blend(self.col_c, self.bar_progress / self.bar_duration)
            c_b = self.col_b.blend(self.col_d, self.bar_progress / self.bar_duration)
        if self.bar_num > 1:
            self.col_a = self.col_c
            self.col_b = self.col_d
            c_a = self.col_a
            c_b = self.col_b

        # beatProc = self.beat_progress / self.beat_duration
        beat_pair_proc = self.beat_pair_progress / self.beat_pair_duration
        # barProc = self.bar_progress / self.bar_duration

        num_modes = 4
        # self.section_num = 2
        if self.section_num % num_modes == 0:
            self.strip.fill_color(Color(r=25, g=25, b=25))
            if self.beat_num % 32 < 24:
                if self.bar_num % 6 < 3:
                    cycle_proc = beat_pair_proc
                else:
                    cycle_proc = 1 - beat_pair_proc
            else:
                cycle_proc = (self.beat_num % 8) / 8
            for i in range(0, self.strip.num_pixels()):
                if i > self.center:
                    self.strip.add_pixel_color(
                        i,
                        Color(r=255, g=255, b=255)
                        * (
                            1
                            / pow(
                                1 + pow((i - self.center - cycle_proc * self.center) / 10, 2),
                                3 / 2,
                            )
                        ),
                    )
                    self.strip.add_pixel_color(
                        i,
                        Color(r=255, g=255, b=255)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center - (cycle_proc + 1) * self.center) / 10,
                                    2,
                                ),
                                3 / 2,
                            )
                        ),
                    )
                else:
                    self.strip.add_pixel_color(
                        i,
                        Color(r=255, g=255, b=255)
                        * (
                            1
                            / pow(
                                1 + pow((i - self.center + cycle_proc * self.center) / 10, 2),
                                3 / 2,
                            )
                        ),
                    )
                    self.strip.add_pixel_color(
                        i,
                        Color(r=255, g=255, b=255)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center + (cycle_proc + 1) * self.center) / 10,
                                    2,
                                ),
                                3 / 2,
                            )
                        ),
                    )

        # Only looks good with time_signature=4
        if self.section_num % num_modes == 1:
            for i in range(0, self.strip.num_pixels()):
                self.brightness[i] *= 0.96
            self.wave_freq = 2
            self.wave_pos += self.wave_vel * (delta / 2)
            if self.beat_num % 4 < 2:
                proc = beat_pair_proc
            else:
                proc = 1 - beat_pair_proc
            for i in range(0, int(self.strip.num_pixels() / 2) + 1):
                ii = i / self.strip.num_pixels()
                self.strip.set_pixel_color(
                    i,
                    Color(r=255, g=255, b=255) * self.brightness[i] * pow(math.sin(ii * math.pi), 3),
                )  # Mask edges
                self.strip.add_pixel_color(
                    i,
                    Color(r=255, g=255, b=255)
                    * (1 - proc)
                    * pow(self.get_bell((i - self.center + proc * self.center) / 10), 2),
                )
                self.strip.set_pixel_color(self.strip.num_pixels() - i - 1, self.strip.get_pixel_color(i))

        if self.section_num % num_modes == 2:
            self.wave_freq = 2
            self.wave_pos += self.wave_vel * delta
            for i in range(0, self.strip.num_pixels()):
                self.brightness[i] *= 0.975
            for i in range(0, self.strip.num_pixels()):
                ii = i / self.strip.num_pixels()
                self.strip.set_pixel_color(
                    i,
                    Color(r=255, g=255, b=255) * self.brightness[i] * pow(math.sin(ii * math.pi), 2),
                )  # Mask edges

        if self.section_num % num_modes == 3:
            for i in range(0, self.strip.num_pixels()):
                self.brightness[i] *= 0.96
            for i in range(0, self.strip.num_pixels()):
                self.strip.set_pixel_color(i, Color(r=255, g=255, b=255) * self.brightness[i])

        for i in range(0, self.strip.num_pixels()):
            ii = ((i - self.strip.num_pixels() / 2) / self.strip.num_pixels()) * math.pi * self.wave_freq
            self.strip.mult_pixel_color(
                i,
                c_a * abs(math.sin(ii + self.wave_pos)) + c_b * abs(math.cos(ii + self.wave_pos)),
            )

    @property
    def depends_on_spotify(self) -> bool:
        return True
