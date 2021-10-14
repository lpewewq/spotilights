import math
import random

from app.lightstrip import RGB
from app.visualizer.spotify_visualizer.base_spotify_visualizer import (
    BaseSpotifyVisualizer,
)


def get_bell(x):
    return 1 / pow(1 + pow(x, 2), 3 / 2)


class State:
    def __init__(self, leds):
        self.leds = leds
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
        self.segment_num = 0
        self.segment_progress = 1
        self.segment_duration = 1
        self.segment_loudness_max_time = 1
        self.segment_loudness_start = 1
        self.segment_loudness_max = 1
        self.segment_loudness_end = 1


class PhilippsSpotifyVisualizer(BaseSpotifyVisualizer):
    def __init__(self, app):
        super().__init__(app)
        self.state = None
        self.center = 0

        # Wave
        self.col_a = RGB(1, 0, 0)
        self.col_b = RGB(0, 1, 0)
        self.col_c = RGB(0, 0, 1)
        self.col_d = RGB(0, 0, 0)
        self.brightness = None
        self.wave_pos = 0
        self.wave_vel = 1
        self.wave_freq = 1

        self.state = State(self.leds)
        self.center = self.state.leds.n_leds / 2
        self.brightness = [RGB(1, 1, 1)] * self.state.leds.n_leds

    def swap_cols(self):
        col_tmp = self.col_a
        self.col_a = self.col_b
        self.col_b = col_tmp
        col_tmp = self.col_c
        self.col_c = self.col_d
        self.col_d = col_tmp

    def section_callback(self, section):
        self.state.sectionLoudness = section["loudness"]
        self.wave_vel = section["tempo"] / 100
        self.wave_freq = 1

        # Center color again
        self.wave_pos = 0
        self.wave_freq = 1

        # Start with first bar
        self.state.bar_num = 0

        # Change colors
        choice = random.randint(0, 3)
        if choice == 0:
            self.col_c = RGB(1, 0, 0)
            self.col_d = RGB(0, 1, 0)
        if choice == 1:
            self.col_c = RGB(1, 0, 0)
            self.col_d = RGB(0, 0, 1)
        if choice == 2:
            self.col_c = RGB(0.1, 1, 0)
            self.col_d = RGB(0, 0, 1)
        if choice == 3:
            self.col_c = RGB(1, 0, 0)
            self.col_d = RGB(1, 1, 0)
        self.wave_pos = 0

        self.state.section_num += 1

    def bar_callback(self, bar):
        self.state.bar_num += 1
        self.state.bar_duration = bar["duration"]
        self.state.bar_progress = 0

    def beat_callback(self, beat):
        self.state.beat_num += 1
        self.state.beat_progress = 0
        self.state.beat_duration = beat["duration"]

        self.swap_cols()

        if self.state.section_num % 4 != 3 and self.state.beat_num % 2 == 1:
            self.brightness = [RGB(1, 1, 1)] * self.state.leds.n_leds
            self.state.beat_pair_progress = 0
            self.state.beat_pair_duration = self.state.beat_duration * 2

        if self.state.section_num % 4 == 3:
            for i in range(0, self.state.leds.n_leds):
                self.brightness[i] += RGB(1, 1, 1) * get_bell(
                    (i - ((self.state.beat_num % 5) / 4) * 287) / 10
                )

    def tatum_callback(self, tatum):
        pass  # tatums are not used

    def segment_callback(self, segment):
        self.state.segment_num += 1
        self.state.segment_progress = 0
        self.state.segment_duration = segment["duration"]
        self.state.segment_loudness_start = segment["loudness_start"]
        self.state.segment_loudness_max = segment["loudness_max"]
        self.state.segment_loudness_end = segment["loudness_end"]
        self.state.segment_loudness_max_time = segment["loudness_max_time"]

    def generic_callback(self, delta):
        self.state.time += delta
        self.state.beat_progress += delta
        self.state.beat_pair_progress += delta
        self.state.segment_progress += delta
        self.state.bar_progress += delta

        # Lerp colors in first bar of section (todo: lerp in HSV, not in RGB)
        if self.state.bar_num == 0:
            c_a = self.col_a.lerp(self.col_c, 0)
            c_b = self.col_b.lerp(self.col_d, 0)
        if self.state.bar_num == 1:
            c_a = self.col_a.lerp(
                self.col_c, self.state.bar_progress / self.state.bar_duration
            )
            c_b = self.col_b.lerp(
                self.col_d, self.state.bar_progress / self.state.bar_duration
            )
        if self.state.bar_num > 1:
            self.col_a = self.col_c
            self.col_b = self.col_d
            c_a = self.col_a
            c_b = self.col_b

        # beatProc = self.state.beat_progress / self.state.beat_duration
        beat_pair_proc = self.state.beat_pair_progress / self.state.beat_pair_duration
        # barProc = self.state.bar_progress / self.state.bar_duration

        num_modes = 4
        # self.section_num = 2
        if self.state.section_num % num_modes == 0:
            self.state.leds.fill(RGB(0.1, 0.1, 0.1))
            if self.state.beat_num % 32 < 24:
                if self.state.bar_num % 6 < 3:
                    cycle_proc = beat_pair_proc
                else:
                    cycle_proc = 1 - beat_pair_proc
            else:
                cycle_proc = (self.state.beat_num % 8) / 8
            for i in range(0, self.state.leds.n_leds):
                if i > self.center:
                    self.state.leds.add_color(
                        i,
                        RGB(1, 1, 1)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center - cycle_proc * self.center) / 10, 2
                                ),
                                3 / 2,
                            )
                        ),
                    )
                    self.state.leds.add_color(
                        i,
                        RGB(1, 1, 1)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center - (cycle_proc + 1) * self.center)
                                    / 10,
                                    2,
                                ),
                                3 / 2,
                            )
                        ),
                    )
                else:
                    self.state.leds.add_color(
                        i,
                        RGB(1, 1, 1)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center + cycle_proc * self.center) / 10, 2
                                ),
                                3 / 2,
                            )
                        ),
                    )
                    self.state.leds.add_color(
                        i,
                        RGB(1, 1, 1)
                        * (
                            1
                            / pow(
                                1
                                + pow(
                                    (i - self.center + (cycle_proc + 1) * self.center)
                                    / 10,
                                    2,
                                ),
                                3 / 2,
                            )
                        ),
                    )

        # Only looks good with time_signature=4
        if self.state.section_num % num_modes == 1:
            for i in range(0, self.state.leds.n_leds):
                self.brightness[i] *= 0.96
            self.wave_freq = 2
            self.wave_pos += self.wave_vel * (delta / 2)
            if self.state.beat_num % 4 < 2:
                proc = beat_pair_proc
            else:
                proc = 1 - beat_pair_proc
            for i in range(0, int(self.state.leds.n_leds / 2) + 1):
                ii = i / self.state.leds.n_leds
                self.state.leds.set_color(
                    i,
                    RGB(1, 1, 1) * self.brightness[i] * pow(math.sin(ii * math.pi), 3),
                )  # Mask edges
                self.state.leds.add_color(
                    i,
                    RGB(1, 1, 1)
                    * (1 - proc)
                    * pow(get_bell((i - self.center + proc * self.center) / 10), 2),
                )
                self.state.leds.set_color(
                    self.state.leds.n_leds - i, self.state.leds.leds[i]
                )

        if self.state.section_num % num_modes == 2:
            self.wave_freq = 2
            self.wave_pos += self.wave_vel * delta
            for i in range(0, self.state.leds.n_leds):
                self.brightness[i] *= 0.975
            for i in range(0, self.state.leds.n_leds):
                ii = i / self.state.leds.n_leds
                self.state.leds.set_color(
                    i, self.brightness[i] * pow(math.sin(ii * math.pi), 2)
                )  # Mask edges

        if self.state.section_num % num_modes == 3:
            for i in range(0, self.state.leds.n_leds):
                self.brightness[i] *= 0.96
            for i in range(0, self.state.leds.n_leds):
                self.state.leds.set_color(i, self.brightness[i])

        for i in range(0, self.state.leds.n_leds):
            ii = (
                ((i - self.state.leds.n_leds / 2) / self.state.leds.n_leds)
                * math.pi
                * self.wave_freq
            )
            self.state.leds.mul_color(
                i,
                c_a * abs(math.sin(ii + self.wave_pos))
                + c_b * abs(math.cos(ii + self.wave_pos)),
            )
