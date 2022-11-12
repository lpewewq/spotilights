import numpy as np
from rpi_ws281x import PixelStrip

from ..abstract import AbstractStrip


class RPIStrip(AbstractStrip):
    def __init__(
        self,
        pin: int,
        freq_hz: int,
        dma: int,
        invert: bool,
        brightness: float,
        channel: int,
        num_pixels: int,
        xy: np.ndarray,
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

    def show(self, colors: np.ndarray) -> None:
        for i, color in enumerate(colors):
            self._rpi_strip.setPixelColor(i, color.as_int())
        self._rpi_strip.show()

    def get_brightness(self) -> int:
        return self._rpi_strip.getBrightness()

    def set_brightness(self, brightness: int) -> None:
        brightness = min(brightness, 255)
        brightness = max(brightness, 0)
        self._rpi_strip.setBrightness(int(brightness))

    def fog_on(self) -> None:
        pass

    def fog_off(self) -> None:
        pass
