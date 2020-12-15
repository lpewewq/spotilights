from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

class RGB:
    r = 0
    g = 0
    b = 0
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return RGB(self.r + other.r, self.g + other.g, self.b + other.b)
    def __mul__(self, other):
        return RGB(self.r * other, self.g * other, self.b * other)
    def __rmul__(self, other):
        return RGB(self.r * other, self.g * other, self.b * other)

class LightstripState:
    connection     = None
    colors         = None
    num_leds       = 0

    def __init__(self, device_path, num_leds):
        self.connection = Serial(device_path, 500000, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=None)
        self.colors = [RGB(0, 0, 0)] * num_leds
        self.num_leds = num_leds

    def show(self):
        # Sanitize data
        for i in range(0, self.num_leds):
            self.colors[i] = RGB(
            min(255, abs(int(self.colors[i].r))),
            min(255, abs(int(self.colors[i].g))),
            min(255, abs(int(self.colors[i].b))))
        # Put new data to LEDs
        self.connection.write(bytes([42, 43, 44, 45, 46]))
        for x in range(0, self.num_leds):
            self.connection.write(bytes([self.colors[x].g, self.colors[x].r, self.colors[x].b]))
