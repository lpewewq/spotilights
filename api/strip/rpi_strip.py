from typing import List

from colour import Color
from rpi_ws281x import Color as rpi_color
from rpi_ws281x import PixelStrip

from .base import LEDStrip


class RpiStrip(LEDStrip):
    def __init__(
        self,
        num: int,
        pin: int,
        freq_hz: int,
        dma: int,
        invert: bool,
        brightness: float,
        channel: int,
    ):
        self._rpi_strip = PixelStrip(
            num=num,
            pin=pin,
            freq_hz=freq_hz,
            dma=dma,
            invert=invert,
            brightness=int(brightness * 255),
            channel=channel,
        )
        self._rpi_strip.begin()
        self.clear()

    def show(self) -> None:
        self._rpi_strip.show()

    def get_pixel_color(self, n: int) -> Color:
        rgb = self._rpi_strip.getPixelColorRGB(n)
        return Color(rgb=(rgb.r / 255, rgb.g / 255, rgb.b / 255))

    def set_pixel_color(self, n: int, color: Color) -> None:
        r, g, b = color.get_red(), color.get_green(), color.get_blue()
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)
        self._rpi_strip.setPixelColor(n, rpi_color(red, green, blue))

    def get_brightness(self) -> int:
        return self._rpi_strip.getBrightness()

    def set_brightness(self, brightness: int) -> None:
        brightness = min(brightness, 255)
        brightness = max(brightness, 0)
        self._rpi_strip.setBrightness(brightness)

    def get_pixels(self) -> List[Color]:
        # TODO getPixels directly
        return [self.get_pixel_color(i) for i in range(self.num_pixels())]

    def num_pixels(self) -> int:
        return self._rpi_strip.numPixels()
