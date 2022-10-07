import warnings

from ..config import settings


if settings.use_backend == "raspberrypi":
    from .concrete.raspberrypi import RPIStrip

    strip = RPIStrip(
        num_pixels=settings.led_count,
        pin=settings.raspi_pin,
        freq_hz=settings.raspi_freq_hz,
        dma=settings.raspi_dma,
        invert=settings.raspi_invert,
        brightness=settings.led_brightness,
        channel=settings.raspi_channel,
        xy=settings.led_2d_coords,
    )
elif settings.use_backend == "arduino":
    from .concrete.arduino import ArduinoStrip

    strip = ArduinoStrip(
        num_pixels=settings.led_count,
        brightness=settings.led_brightness,
        port=settings.arduino_serial_port,
        baudrate=settings.arduino_serial_baudrate,
        header=settings.arduino_serial_header,
        xy=settings.led_2d_coords,
    )
else:
    warnings.warn("Unknown LED strip backend!")
