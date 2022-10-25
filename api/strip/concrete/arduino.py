import numpy as np
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial
from serial.serialutil import SerialException
from serial.tools import list_ports

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
        while True:
            try:
                self.serial_connection = Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=EIGHTBITS,
                    parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE,
                    timeout=None,
                )
                break
            except SerialException as e:
                print(e)
                print("Choose other port:")
                port_list = list_ports.comports()
                for i, p in enumerate(port_list):
                    print(f"{i}: {p}")
                i = int(input())
                port = port_list[i].device
        self.clear()

    def clear(self):
        # problem: show is canceled while sending data
        # more robust if cleared multiple times
        for _ in range(5):
            super().clear()

    def show(self, colors: np.ndarray) -> None:
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
