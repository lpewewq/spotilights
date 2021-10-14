from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class SerialController:
    def __init__(self, app):
        self.header = [42, 43, 44, 45, 46]
        port = app.config["SERIAL_PORT"]
        baud_rate = app.config["BAUD_RATE"]
        self.serial_connection = Serial(
            port,
            baud_rate,
            EIGHTBITS,
            PARITY_NONE,
            STOPBITS_ONE,
            timeout=None,
        )

    def write(self, lightstrip):
        # scale and clamp r,g,b values and apply color correction
        clamp = lambda x, m: min(m, max(0, int(m * x)))
        self.serial_connection.write(bytes(self.header))
        for led in lightstrip.leds:
            r = clamp(led.r, 255)
            g = clamp(led.b, 176)
            b = clamp(led.g, 246)
            # WS2812B use GRB
            self.serial_connection.write(bytes([g, r, b]))
