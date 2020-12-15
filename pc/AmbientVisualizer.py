from LightstripState import RGB
import math

class AmbientVisualizer:
    colA       = RGB(0, 0, 255)
    colB       = RGB(0, 255, 0)
    brightness = 1
    wavePos    = 0

    def callback(self, leds, delta):
        self.wavePos += delta / 2
        for i in range(0, leds.num_leds):
            ii = i / leds.num_leds * math.pi
            leds.colors[i] = (self.colA * abs(math.sin(ii + self.wavePos)) + self.colB * abs(math.cos(ii + self.wavePos))) * self.brightness
