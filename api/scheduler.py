import asyncio
import ctypes as ct
import time
from colorsys import hsv_to_rgb

import numpy as np
from rpi_ws281x import Color


def to_byte(value: float, lower=0.0, upper=1.0):
    res = min(value, upper)
    res = max(lower, res)
    return int(res * 255)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


async def rainbow(strip, delay):
    while True:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            await asyncio.sleep(delay)


async def theater(strip, delay):
    while True:
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                strip.show()
                await asyncio.sleep(delay)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)


async def fill(strip, color):
    while True:
        strip.fillColor(color)
        strip.show()
        await asyncio.sleep(1)


async def pride(strip):
    # Adapted from https://github.com/FastLED/FastLED/tree/b5874b588ade1d2639925e4e9719fa7d3c9d9e94/examples/Pride2015

    def beatsin88(bpm, lowest, highest):
        beat = time.time() * np.pi * bpm / 7680
        beatsin = (np.sin(beat) + 1) / 2
        rangewidth = highest - lowest
        return int(lowest + rangewidth * beatsin)

    sPseudotime = ct.c_uint16(0)
    sLastMillis = time.time() * 1000
    sHue16 = ct.c_uint16(0)

    while True:
        sat8 = ct.c_uint8(beatsin88(87, 220, 250))
        brightdepth = ct.c_uint8(beatsin88(341, 96, 224))
        brightnessthetainc16 = ct.c_uint16(beatsin88(203, 6400, 10240))
        msmultiplier = ct.c_uint8(beatsin88(147, 23, 60))

        hue16 = ct.c_uint16(sHue16.value)
        hueinc16 = ct.c_uint16(beatsin88(113, 1, 3000))

        ms = time.time() * 1000
        deltams = ct.c_uint16(int(ms - sLastMillis))
        sLastMillis = ms
        sPseudotime = ct.c_uint16(sPseudotime.value + deltams.value * msmultiplier.value)
        sHue16 = ct.c_uint16(sHue16.value + deltams.value * beatsin88(400, 5, 9))
        brightnesstheta16 = ct.c_uint16(sPseudotime.value)

        for i in range(strip.numPixels()):
            hue16 = ct.c_uint16(hue16.value + hueinc16.value)
            hue8 = ct.c_uint8(hue16.value // 256)

            brightnesstheta16 = ct.c_uint16(brightnesstheta16.value + brightnessthetainc16.value)
            b16 = ct.c_uint16(int((np.sin(np.pi * (brightnesstheta16.value / 32768)) + 1) * 32768))

            bri16 = ct.c_uint16((b16.value * b16.value) // 65536)
            bri8 = ct.c_uint8((bri16.value * brightdepth.value) // 65536)
            bri8 = ct.c_uint8(bri8.value + 255 - brightdepth.value)
            r, g, b = hsv_to_rgb(hue8.value / 255, sat8.value / 255, bri8.value / 255)

            color = strip.getPixelColorRGB(i)
            r = (3 * r + color.r / 255) / 4
            g = (3 * g + color.g / 255) / 4
            b = (3 * b + color.b / 255) / 4
            strip.setPixelColorRGB(i, to_byte(r), to_byte(g), to_byte(b))
        strip.show()
        await asyncio.sleep(0)
