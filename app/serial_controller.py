from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class SerialController:
    def __init__(self, app):
        self.header = [42, 43, 44, 45, 46]
        self.brightness = 0.5
        self.serial_connection = Serial(
            app.config["SERIAL_PORT"],
            app.config["BAUD_RATE"],
            EIGHTBITS,
            PARITY_NONE,
            STOPBITS_ONE,
            timeout=None,
        )

    def write(self, lightstrip):
        # scale and clamp r,g,b values and apply color correction
        clamp = lambda x, m: min(int(m), max(0, int(m * x)))
        self.serial_connection.write(bytes(self.header))
        for led in lightstrip.leds:
            # color correction
            r = clamp(led.r, 255 * self.brightness)
            g = clamp(led.b, 176 * self.brightness)
            b = clamp(led.g, 246 * self.brightness)
            # WS2812B use GRB
            self.serial_connection.write(bytes([g, r, b]))
