from rpi_ws281x import Color, PixelStrip
import asyncio

from .config import settings


class LEDStrip(PixelStrip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin()
        self.animation_task = None
        self.fillColor(Color(0, 0, 0))
        self.show()

    def start_animation(self, animation_function, *args):
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()
        self.animation_task = asyncio.create_task(animation_function(self, *args))

    def fillColor(self, color):
        for i in range(self.numPixels()):
            self.setPixelColor(i, color)


strip = LEDStrip(
    num=settings.led_count,
    pin=settings.led_pin,
    freq_hz=settings.led_freq_hz,
    dma=settings.led_dma,
    invert=settings.led_invert,
    brightness=settings.led_brightness,
    channel=settings.led_channel,
)
