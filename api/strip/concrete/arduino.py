from typing import Any, List

from ...color import Color
from ..base import ShowableStrip
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class ArduinoStrip(ShowableStrip):
    def __init__(self, num: int, brightness: float, port: Any, baudrate: int, header: List[int]):
        self.data = [Color(r=0, g=0, b=0) for i in range(num)]
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
        self.show()

    def show(self) -> None:
        self.serial_connection.write(self.header)
        for color in self.data:
            r, g, b = (color * self.brightness).as_bytes()
            # WS2812B uses GRB
            self.serial_connection.write(bytes([g, r, b]))

    def get_pixel_color(self, n: int) -> Color:
        return self.data[n]

    def set_pixel_color(self, n: int, color: Color) -> None:
        self.data[n] = color

    def get_brightness(self) -> int:
        return int(self.brightness * 255)

    def set_brightness(self, brightness: int) -> None:
        self.brightness = brightness / 255

    def get_pixels(self) -> List[Color]:
        return self.data

    def num_pixels(self) -> int:
        return len(self.data)
