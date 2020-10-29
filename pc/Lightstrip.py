from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import threading
import time

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
    startTime      = 0
    lastUpdate      = 0
    updateCallback = None
    thread         = None

    def __init__(self, device_path, num_leds):
        self.connection = Serial(device_path, 500000, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=None)
        self.colors = [RGB(0, 0, 0)] * num_leds
        self.num_leds = num_leds

    def startVisualization(self, updateCallback):
        self.updateCallback = updateCallback
        self.thread = StoppableThread(target = self.loop, args = [])
        self.startTime = time.time()
        self.lastUpdate = self.startTime
        self.thread.start()

    def endVisualization(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread.join()
            self.thread = None

    def show(self):
        # Put new data to LEDs
        self.connection.write(bytes([42, 43, 44, 45, 46]))
        for x in range(0, self.num_leds):
            self.connection.write(bytes([self.colors[x].g, self.colors[x].r, self.colors[x].b]))

    def loop(self):
        while not self.thread.stopped():
            now = time.time()
            delta = now - self.lastUpdate
            self.lastUpdate = now
            self.updateCallback(self, delta)
            self.show()

class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
        