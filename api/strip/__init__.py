from ..config import settings, StripBackend

if settings.use_backend == StripBackend.raspberrypi:
    from .concrete.raspberrypi import RPIStrip

    strip = RPIStrip(
        num_pixels=settings.led_count,
        xy=settings.led_2d_coords,
        pin=settings.raspi_pin,
        freq_hz=settings.raspi_freq_hz,
        dma=settings.raspi_dma,
        invert=settings.raspi_invert,
        brightness=settings.led_brightness,
        channel=settings.raspi_channel,
    )
elif settings.use_backend == StripBackend.arduino:
    from .concrete.arduino import ArduinoStrip

    strip = ArduinoStrip(
        num_pixels=settings.led_count,
        xy=settings.led_2d_coords,
        brightness=settings.led_brightness,
        port=settings.arduino_serial_port,
        baudrate=settings.arduino_serial_baudrate,
        header=settings.arduino_serial_header,
    )
