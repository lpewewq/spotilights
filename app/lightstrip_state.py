from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial


def lerp(a, b, p):
    return a + (b - a) * p


class RGB:
    r = 0
    g = 0
    b = 0

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return RGB(self.r + other.r, self.g + other.g, self.b + other.b)
        return RGB(self.r + other, self.g + other, self.b + other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return RGB(self.r * other.r, self.g * other.g, self.b * other.b)
        return RGB(self.r * other, self.g * other, self.b * other)

    def lerp(self, other, percentage):
        return RGB(
            lerp(self.r, other.r, percentage),
            lerp(self.g, other.g, percentage),
            lerp(self.b, other.b, percentage),
        )


class LightstripState:
    header = [42, 43, 44, 45, 46]

    def __init__(self, app):
        self.connection = Serial(
            app.config["SERIAL_PORT"],
            500000,
            EIGHTBITS,
            PARITY_NONE,
            STOPBITS_ONE,
            timeout=None,
        )
        self.n_leds = app.config["N_LEDS"]
        self.clear()

    def show(self, audio_filter):
        power = audio_filter.lowpass_power()
        # soften the brightness
        power = (1 + 9 * power) / 10
        # Put new data to LEDs
        self.connection.write(bytes(self.header))
        for i in range(0, self.n_leds):
            r = int(255 * self.colors[i].r * power)
            b = int(255 * self.colors[i].g * power)
            g = int(255 * self.colors[i].b * power)
            self.connection.write(bytes([g, r, b]))

    def fill(self, color):
        self.colors = [color for _ in range(0, self.n_leds)]

    def clear(self):
        self.fill(RGB(0, 0, 0))

    def invert(self):
        for i in range(0, self.n_leds):
            self.colors[i] = RGB(
                1 - self.colors[i].r, 1 - self.colors[i].g, 1 - self.colors[i].b
            )

    def set_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.colors[int(index)] = color
        self.sanitize(int(index))

    def add_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.colors[int(index)] += color
        self.sanitize(int(index))

    def mul_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.colors[int(index)] *= color
        self.sanitize(int(index))

    def sanitize(self, index):
        self.colors[index] = RGB(
            min(1, abs(self.colors[index].r)),
            min(1, abs(self.colors[index].g)),
            min(1, abs(self.colors[index].b)),
        )
