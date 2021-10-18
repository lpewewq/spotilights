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

    def __repr__(self) -> str:
        return f"RGB {self.r} {self.g} {self.b}"

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


class Lightstrip:
    def __init__(self, app):
        self.n_leds = app.config["N_LEDS"]
        self.leds = [RGB(0, 0, 0) for _ in range(0, self.n_leds)]

    def fill(self, color):
        self.leds = [color for _ in range(0, self.n_leds)]

    def clear(self):
        self.fill(RGB(0, 0, 0))

    def invert(self):
        for i in range(0, self.n_leds):
            self.leds[i] = RGB(
                1 - self.leds[i].r, 1 - self.leds[i].g, 1 - self.leds[i].b
            )

    def set_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.leds[int(index)] = color
        self.sanitize(int(index))

    def add_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.leds[int(index)] += color
        self.sanitize(int(index))

    def mul_color(self, index, color):
        if int(index) < 0 or int(index) >= self.n_leds:
            return
        self.leds[int(index)] *= color
        self.sanitize(int(index))

    def sanitize(self, index):
        self.leds[index] = RGB(
            min(1, abs(self.leds[index].r)),
            min(1, abs(self.leds[index].g)),
            min(1, abs(self.leds[index].b)),
        )
