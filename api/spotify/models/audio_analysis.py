from dataclasses import dataclass
from typing import Optional

import numpy as np
import tekore as tk
from scipy import interpolate
from scipy.signal.windows import gaussian

from ...config import settings


def convert_loudness(loudness: float) -> float:
    return 1 + loudness / 60


@dataclass(repr=False)
class Section(tk.model.Section):
    next: Optional["Section"] = None

    def __post_init__(self):
        self.loudness = convert_loudness(self.loudness)


@dataclass(repr=False)
class Bar(tk.model.TimeInterval):
    next: Optional["Bar"] = None


@dataclass(repr=False)
class Beat(tk.model.TimeInterval):
    next: Optional["Beat"] = None


@dataclass(repr=False)
class Tatum(tk.model.TimeInterval):
    next: Optional["Tatum"] = None


@dataclass(repr=False)
class Segment(tk.model.Segment):
    next: Optional["Segment"] = None
    loudness_start_smoothed: float = 0
    loudness_start_gradient: float = 0
    loudness_start_gradient_suppressed: float = 0

    def __post_init__(self):
        self.loudness_start = convert_loudness(self.loudness_start)
        self.loudness_max = convert_loudness(self.loudness_max)
        self.loudness_end = convert_loudness(self.loudness_end)


@dataclass(repr=False)
class AudioAnalysis:
    duration: float
    end_of_fade_in: float
    start_of_fade_out: float
    loudness: float
    tempo: float
    sections: list[Section]
    bars: list[Bar]
    beats: list[Beat]
    tatums: list[Tatum]
    segments: list[Segment]
    loudness_interpolation: interpolate.interp1d

    @classmethod
    def from_tekore(cls, audio_analysis: tk.model.AudioAnalysis) -> "AudioAnalysis":
        track = audio_analysis.track
        duration = track["duration"]
        end_of_fade_in = track["end_of_fade_in"]
        start_of_fade_out = track["start_of_fade_out"]
        loudness = track["loudness"]
        tempo = track["tempo"]

        sections = [Section(**s.__dict__) for s in audio_analysis.sections]
        bars = [Bar(**b.__dict__) for b in audio_analysis.bars]
        beats = [Beat(**b.__dict__) for b in audio_analysis.beats]
        tatums = [Tatum(**t.__dict__) for t in audio_analysis.tatums]
        segments = [Segment(**s.__dict__) for s in audio_analysis.segments]

        # interpolate loudness
        resample_rate = settings.segment_loudness_resample_rate
        segment_loudnesses = np.array([[s.start, s.loudness_start] for s in segments])
        x = segment_loudnesses[:, 0]
        y = segment_loudnesses[:, 1]
        x_resampled = np.arange(x[0], x[-1], 1 / resample_rate)
        y_resampled = interpolate.interp1d(x, y)(x_resampled)

        # smooth loudness
        M = int(resample_rate * settings.segment_loudness_smoothing_kernel_size)
        smoothing_kernel = gaussian(M, M / 4)
        smoothing_kernel /= smoothing_kernel.sum()
        y_smoothed = np.convolve(y_resampled, smoothing_kernel, mode="same")
        # y_smoothed -= y_smoothed.min()
        y_smoothed /= y_smoothed.max()  # clamp to 1

        # loudness gradients
        y_gradients = np.gradient(y_smoothed, 1.0 / resample_rate)

        # downsample
        down_indicies = [round((len(x_resampled) - 1) * (t - x[0]) / (x[-1] - x[0])) for t in x]
        y_gradients_down = y_gradients[down_indicies]
        y_smoothed_down = y_smoothed[down_indicies]

        # non extram suppression
        y_gradients_down_supr = np.zeros(len(y_gradients_down))
        for i in range(1, len(y_gradients_down) - 1):
            if y_gradients_down[i - 1] < y_gradients_down[i] and y_gradients_down[i] > y_gradients_down[i + 1]:
                y_gradients_down_supr[i] = y_gradients_down[i]
            elif y_gradients_down[i - 1] > y_gradients_down[i] and y_gradients_down[i] < y_gradients_down[i + 1]:
                y_gradients_down_supr[i] = y_gradients_down[i]

        for s, smoothed, gradient, gradient_supr in zip(segments, y_smoothed_down, y_gradients_down, y_gradients_down_supr):
            s.loudness_start_smoothed = smoothed
            s.loudness_start_gradient = gradient
            s.loudness_start_gradient_suppressed = gradient_supr

        # plotting
        # import time

        # import matplotlib
        # import matplotlib.pyplot as plt

        # plt.rcParams["figure.figsize"] = [100, 5]
        # plt.rcParams["figure.autolayout"] = True
        # fig, ax = plt.subplots()
        # ax.plot(x, y, label="OG")
        # ax.plot(x_resampled, y_resampled, label="Interpolated")
        # ax.plot(x_resampled, y_smoothed, label="Smoothed (Clamped to 1)")
        # ax.plot(x_resampled, y_gradients, label="Gradients")
        # ax.plot(x, y_gradients_down, label="Gradients Downsampled")
        # ax.plot(x, y_gradients_down_supr, label="Gradients Downsampled NES")
        # ax.hlines(0.3, x[0], x[-1], label="Strobe Threshold")
        # ax.legend()
        # formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime("%M:%S", time.gmtime(s)))
        # ax.set_ylim(-1, 1)
        # ax.xaxis.set_major_formatter(formatter)
        # ax.xaxis.set_ticks(np.arange(min(x), max(x) + 1, 5))
        # fig.savefig("segment_loudness.png", dpi=75)

        for l in [sections, bars, beats, tatums, segments]:
            for i, next_i in zip(l, l[1:]):
                i.next = next_i

        loudness_interpolation = interpolate.interp1d(x, y_smoothed_down)
        return AudioAnalysis(
            duration=duration,
            end_of_fade_in=end_of_fade_in,
            start_of_fade_out=start_of_fade_out,
            loudness=loudness,
            tempo=tempo,
            sections=sections,
            bars=bars,
            beats=beats,
            tatums=tatums,
            segments=segments,
            loudness_interpolation=loudness_interpolation,
        )
