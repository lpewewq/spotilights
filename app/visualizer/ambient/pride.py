# Inspired by https://github.com/FastLED/FastLED/tree/b5874b588ade1d2639925e4e9719fa7d3c9d9e94/examples/Pride2015

import ctypes as ct
import time
from colorsys import hsv_to_rgb

import numpy as np
from app.visualizer import RGB
from app.visualizer.base import BaseVisualizer


def beatsin(bpm, lowest=0.0, highest=1.0):
    beat = time.time() * np.pi * bpm / 30
    beatsin = (np.sin(beat) + 1) / 2
    rangewidth = highest - lowest
    return lowest + rangewidth * beatsin


class PrideVisualizer(BaseVisualizer):
    def __init__(self, app):
        super().__init__(app)
        self.sPseudotime = ct.c_uint16(0)
        self.sHue16 = ct.c_uint16(0)
        self.fps = 60

    def update(self, delta):
        deltams = ct.c_uint16(int(delta * 1000))

        sat8 = ct.c_uint8(int(beatsin(0.3, 220, 250)))
        brightdepth = ct.c_uint8(int(beatsin(1.3, 96, 224)))
        brightnessthetainc16 = ct.c_uint16(int(beatsin(0.8, 6400, 10240)))
        msmultiplier = ct.c_uint8(int(beatsin(0.6, 23, 60)))

        hue16 = ct.c_uint16(self.sHue16.value)
        hueinc16 = ct.c_uint16(int(beatsin(0.4, 1, 3000)))

        self.sPseudotime = ct.c_uint16(
            self.sPseudotime.value + deltams.value * msmultiplier.value
        )
        self.sHue16 = ct.c_uint16(
            self.sHue16.value + deltams.value * int(beatsin(1.6, 5, 9))
        )
        brightnesstheta16 = ct.c_uint16(self.sPseudotime.value)

        for led in self.leds.leds:
            hue16 = ct.c_uint16(hue16.value + hueinc16.value)
            hue8 = ct.c_uint8(int(hue16.value / 256))

            brightnesstheta16 = ct.c_uint16(
                brightnesstheta16.value + brightnessthetainc16.value
            )
            b16 = ct.c_uint16(
                int(np.sin(np.pi * (brightnesstheta16.value / 32768)) + 1 * 32768)
            )

            bri16 = ct.c_uint16(int((b16.value * b16.value) / 65536))
            bri8 = ct.c_uint8(int((bri16.value * brightdepth.value) / 65536))
            bri8 = ct.c_uint8(bri8.value + (255 - brightdepth.value))
            newcolor = RGB(
                *hsv_to_rgb(hue8.value / 255, sat8.value / 255, bri8.value / 255)
            )

            led.r = (3 * led.r + newcolor.r) / 4
            led.g = (3 * led.g + newcolor.g) / 4
            led.b = (3 * led.b + newcolor.b) / 4
        time.sleep(1.0 / self.fps)
        return self.leds
