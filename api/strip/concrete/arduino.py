from ...color import Color
from ..base import GlobalStrip
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class ArduinoStrip(GlobalStrip):
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
        self.data = [Color(r=0, g=0, b=0) for i in range(num_pixels)]
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

    def get_pixel_color(self, i: int) -> Color:
        return self.data[i]

    def set_pixel_color(self, i: int, color: Color) -> None:
        self.data[i] = color

    def get_brightness(self) -> int:
        return int(self.brightness * 255)

    def set_brightness(self, brightness: int) -> None:
        self.brightness = brightness / 255

    def get_pixels(self) -> list[Color]:
        return self.data
