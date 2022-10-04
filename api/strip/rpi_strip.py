from typing import List

from rpi_ws281x import Color as rpi_color
from rpi_ws281x import PixelStrip

from ..color import Color
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
        return Color.from_int(self._rpi_strip.getPixelColor(n))

    def set_pixel_color(self, n: int, color: Color) -> None:
        self._rpi_strip.setPixelColor(n, color.as_int())

    def get_brightness(self) -> int:
        return self._rpi_strip.getBrightness()

    def set_brightness(self, brightness: int) -> None:
        brightness = min(brightness, 255)
        brightness = max(brightness, 0)
        self._rpi_strip.setBrightness(int(brightness))

    def get_pixels(self) -> List[Color]:
        return [Color.from_int(x) for x in self._rpi_strip.getPixels()[:]]

    def num_pixels(self) -> int:
        return self._rpi_strip.numPixels()
