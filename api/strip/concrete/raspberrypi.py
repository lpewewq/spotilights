from rpi_ws281x import PixelStrip

from ...color import Color
from ..base import GlobalStrip


class RPIStrip(GlobalStrip):
    def __init__(
        self,
        pin: int,
        freq_hz: int,
        dma: int,
        invert: bool,
        brightness: float,
        channel: int,
        num_pixels: int,
        xy: list[tuple[float, float]] = None,
    ) -> None:
        super().__init__(num_pixels, xy)
        self._rpi_strip = PixelStrip(
            num=num_pixels,
            pin=pin,
            freq_hz=freq_hz,
            dma=dma,
            invert=invert,
            brightness=int(brightness * 255),
            channel=channel,
        )
        self._rpi_strip.begin()
        self.clear()
        self.show()

    def show(self) -> None:
        self._rpi_strip.show()

    def get_pixel_color(self, i: int) -> Color:
        return Color.from_int(self._rpi_strip.getPixelColor(i))

    def set_pixel_color(self, i: int, color: Color) -> None:
        self._rpi_strip.setPixelColor(i, color.as_int())

    def get_brightness(self) -> int:
        return self._rpi_strip.getBrightness()

    def set_brightness(self, brightness: int) -> None:
        brightness = min(brightness, 255)
        brightness = max(brightness, 0)
        self._rpi_strip.setBrightness(int(brightness))

    def get_pixels(self) -> list[Color]:
        return [Color.from_int(x) for x in self._rpi_strip.getPixels()[:]]
