from LightstripState import RGB
import math

class AmbientVisualizer:
    leds       = None
    colA       = RGB(0, 255, 0)
    colB       = RGB(0, 0, 0)
    brightness = 0.5
    wavePos    = 0

    def __init__(self, leds):
        self.leds = leds

    def callback(self, delta):
        self.wavePos += delta / 2
        for i in range(0, self.leds.num_leds):
            ii = i / self.leds.num_leds * math.pi
            self.leds.colors[i] = (self.colA * abs(math.sin(ii + self.wavePos)) + self.colB * abs(math.cos(ii + self.wavePos))) * self.brightness
