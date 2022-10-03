from ..config import settings
from .base import LEDStrip
from .rpi_strip import RpiStrip

strip = RpiStrip(
    num=settings.led_count,
    pin=settings.led_pin,
    freq_hz=settings.led_freq_hz,
    dma=settings.led_dma,
    invert=settings.led_invert,
    brightness=settings.led_brightness,
    channel=settings.led_channel,
)
