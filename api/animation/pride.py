import ctypes as ct
import time
from typing import Literal

import numpy as np

from ..color import Color
from .abstract import AbstractAnimation
from .decorators import save_previous


class Pride(AbstractAnimation):
    """Complex rainbow animation."""

    name: Literal["Pride"]
    _sPseudotime = ct.c_uint16(0)
    _sHue16 = ct.c_uint16(0)
    _sLastMillis = time.time() * 1000

    @property
    def needs_spotify(self) -> bool:
        return False

    def beatsin88(self, bpm, lowest, highest) -> int:
        beat = time.time() * np.pi * bpm / 7680
        beatsin = (np.sin(beat) + 1) / 2
        rangewidth = highest - lowest
        return int(lowest + rangewidth * beatsin)

    @save_previous
    def render(self, progress: float, xy: np.ndarray, previous: np.ndarray) -> np.ndarray:
        sat8 = ct.c_uint8(self.beatsin88(87, 220, 250))
        brightdepth = ct.c_uint8(self.beatsin88(341, 96, 224))
        brightnessthetainc16 = ct.c_uint16(self.beatsin88(203, 6400, 10240))
        msmultiplier = ct.c_uint8(self.beatsin88(147, 23, 60))

        hue16 = ct.c_uint16(self._sHue16.value)
        hueinc16 = ct.c_uint16(self.beatsin88(113, 1, 3000))

        ms = time.time() * 1000
        deltams = ct.c_uint16(int(ms - self._sLastMillis))
        self._sLastMillis = ms
        self._sPseudotime = ct.c_uint16(self._sPseudotime.value + deltams.value * msmultiplier.value)
        self._sHue16 = ct.c_uint16(self._sHue16.value + deltams.value * self.beatsin88(400, 5, 9))
        brightnesstheta16 = ct.c_uint16(self._sPseudotime.value)

        n = len(xy)
        colors = np.empty(n, dtype=Color)
        for i in range(n):
            hue16 = ct.c_uint16(hue16.value + hueinc16.value)
            hue8 = ct.c_uint8(hue16.value // 256)

            brightnesstheta16 = ct.c_uint16(brightnesstheta16.value + brightnessthetainc16.value)
            b16 = ct.c_uint16(int((np.sin(np.pi * (brightnesstheta16.value / 32768)) + 1) * 32768))

            bri16 = ct.c_uint16((b16.value * b16.value) // 65536)
            bri8 = ct.c_uint8((bri16.value * brightdepth.value) // 65536)
            bri8 = ct.c_uint8(bri8.value + 255 - brightdepth.value)
            colors[i] = Color.from_hsv(hue8.value / 255, sat8.value / 255, bri8.value / 255)

        return Color.lerp(colors, previous, 0.25)
