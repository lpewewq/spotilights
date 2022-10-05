import warnings

from ..config import settings
from .concrete import ArduinoStrip, RPIStrip

if settings.use_backend == "raspberrypi":
    strip = RPIStrip(
        num=settings.led_count,
        pin=settings.raspi_pin,
        freq_hz=settings.raspi_freq_hz,
        dma=settings.raspi_dma,
        invert=settings.raspi_invert,
        brightness=settings.led_brightness,
        channel=settings.raspi_channel,
    )
elif settings.use_backend == "arduino":
    strip = ArduinoStrip(
        num=settings.led_count,
        brightness=settings.led_brightness,
        port=settings.arduino_serial_port,
        baudrate=settings.arduino_serial_baudrate,
        header=settings.arduino_serial_header,
    )
else:
    warnings.warn("Unknown LED strip backend!")
