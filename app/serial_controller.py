from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


class SerialController:
    header = [42, 43, 44, 45, 46]

    def __init__(self, app):
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
        # scale and clamp values from [0, 1] to [0, 255]
        clamp_to_byte = lambda x: min(255, max(0, int(255 * x)))
        self.serial_connection.write(bytes(self.header))
        for led in lightstrip.leds:
            r = clamp_to_byte(led.r)
            b = clamp_to_byte(led.g)
            g = clamp_to_byte(led.b)
            self.serial_connection.write(bytes([g, r, b]))
