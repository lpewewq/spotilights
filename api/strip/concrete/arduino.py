import numpy as np
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

from ..abstract import AbstractStrip


class ArduinoStrip(AbstractStrip):
    def __init__(
        self,
        brightness: float,
        port: str,
        baudrate: int,
        header: list[int],
        num_pixels: int,
        xy: list[tuple[float, float]] = None,
    ) -> None:
        super().__init__(num_pixels, xy)
        self.header = bytes(header)
        self.brightness = brightness
        self.serial_connection = Serial(
            port=port,
            baudrate=baudrate,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=None,
        )
        self.clear()

    def show(self,  colors: np.ndarray) -> None:
        self.serial_connection.write(self.header)
        for color in colors:
            r, g, b = (color * self.brightness).as_bytes()
            # WS2812B uses GRB
            self.serial_connection.write(bytes([g, r, b]))

    def get_brightness(self) -> int:
        return int(self.brightness * 255)

    def set_brightness(self, brightness: int) -> None:
        brightness = min(brightness, 255)
        brightness = max(brightness, 0)
        self.brightness = brightness / 255
