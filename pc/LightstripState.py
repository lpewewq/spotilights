from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

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
    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            return RGB(self.r * other.r, self.g * other.g, self.b * other.b)
        return RGB(self.r * other, self.g * other, self.b * other)

    def lerp(self, other, percentage):
        return RGB(lerp(self.r, other.r, percentage), lerp(self.g, other.g, percentage), lerp(self.b, other.b, percentage))

class LightstripState:
    connection     = None
    colors         = None
    num_leds       = 0

    def __init__(self, device_path, num_leds):
        self.connection = Serial(device_path, 500000, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=None)
        self.colors = [RGB(0, 0, 0)] * num_leds
        self.num_leds = num_leds

    def show(self):
        # Put new data to LEDs
        self.connection.write(bytes([42, 43, 44, 45, 46]))
        for i in range(0, self.num_leds):
            self.connection.write(bytes([int(255 * self.colors[i].g), int(255 * self.colors[i].r), int(255 * self.colors[i].b)]))

    def fill(self, color):
        for i in range(0, self.num_leds):
            self.colors[i] = color

    def invert(self):
        for i in range(0, self.num_leds):
            self.colors[i] = RGB(1 - self.colors[i].r, 1 - self.colors[i].g, 1 - self.colors[i].b)

    def setColor(self, index, color):
        if (int(index) < 0 or int(index) >= self.num_leds):
            return
        self.colors[int(index)] = color
        self.sanitize(int(index))

    def addColor(self, index, color):
        if (int(index) < 0 or int(index) >= self.num_leds):
            return
        self.colors[int(index)] += color
        self.sanitize(int(index))

    def mulColor(self, index, color):
        if (int(index) < 0 or int(index) >= self.num_leds):
            return
        self.colors[int(index)] *= color
        self.sanitize(int(index))

    def sanitize(self, index):
        self.colors[index] = RGB(
            min(1, abs(self.colors[index].r)),
            min(1, abs(self.colors[index].g)),
            min(1, abs(self.colors[index].b)))
