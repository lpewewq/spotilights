import ctypes as ct
import time
from colorsys import hsv_to_rgb

import numpy as np

from .base import BaseAnimation


class PrideAnimation(BaseAnimation):
    def __init__(self, strip: "LEDStrip") -> None:
        super().__init__(strip)
        self.sPseudotime = ct.c_uint16(0)
        self.sLastMillis = time.time() * 1000
        self.sHue16 = ct.c_uint16(0)

    def to_byte(self, value: float, lower=0.0, upper=1.0) -> int:
        res = min(value, upper)
        res = max(lower, res)
        return int(res * 255)

    def beatsin88(self, bpm, lowest, highest) -> int:
        beat = time.time() * np.pi * bpm / 7680
        beatsin = (np.sin(beat) + 1) / 2
        rangewidth = highest - lowest
        return int(lowest + rangewidth * beatsin)

    async def loop(self) -> None:
        sat8 = ct.c_uint8(self.beatsin88(87, 220, 250))
        brightdepth = ct.c_uint8(self.beatsin88(341, 96, 224))
        brightnessthetainc16 = ct.c_uint16(self.beatsin88(203, 6400, 10240))
        msmultiplier = ct.c_uint8(self.beatsin88(147, 23, 60))

        hue16 = ct.c_uint16(self.sHue16.value)
        hueinc16 = ct.c_uint16(self.beatsin88(113, 1, 3000))

        ms = time.time() * 1000
        deltams = ct.c_uint16(int(ms - self.sLastMillis))
        self.sLastMillis = ms
        self.sPseudotime = ct.c_uint16(
            self.sPseudotime.value + deltams.value * msmultiplier.value
        )
        self.sHue16 = ct.c_uint16(
            self.sHue16.value + deltams.value * self.beatsin88(400, 5, 9)
        )
        brightnesstheta16 = ct.c_uint16(self.sPseudotime.value)

        for i in range(self.strip.numPixels()):
            hue16 = ct.c_uint16(hue16.value + hueinc16.value)
            hue8 = ct.c_uint8(hue16.value // 256)

            brightnesstheta16 = ct.c_uint16(
                brightnesstheta16.value + brightnessthetainc16.value
            )
            b16 = ct.c_uint16(
                int((np.sin(np.pi * (brightnesstheta16.value / 32768)) + 1) * 32768)
            )

            bri16 = ct.c_uint16((b16.value * b16.value) // 65536)
            bri8 = ct.c_uint8((bri16.value * brightdepth.value) // 65536)
            bri8 = ct.c_uint8(bri8.value + 255 - brightdepth.value)
            r, g, b = hsv_to_rgb(hue8.value / 255, sat8.value / 255, bri8.value / 255)

            color = self.strip.getPixelColorRGB(i)
            r = (3 * r + color.r / 255) / 4
            g = (3 * g + color.g / 255) / 4
            b = (3 * b + color.b / 255) / 4
            self.strip.setPixelColorRGB(
                i, self.to_byte(r), self.to_byte(g), self.to_byte(b)
            )
        self.strip.show()
