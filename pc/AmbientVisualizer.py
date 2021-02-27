from LightstripState import RGB
import colorsys
import math

class AmbientVisualizer:
    colA       = RGB(1, 0, 0)
    colB       = RGB(1, 1, 0)
    brightness = 1
    wavePos    = 0
    leds       = None

    def __init__(self, leds):
        self.leds = leds

    def callback(self, delta):
        self.wavePos += delta / 5
        for i in range(0, self.leds.numLEDs):
            ii = i / self.leds.numLEDs # * math.pi
            #self.leds.setColor(i,
                #pow(math.sin(ii * math.pi), 3) * (self.colA * abs(math.sin(ii + self.wavePos)) + self.colB * abs(math.cos(ii + self.wavePos))) * self.brightness)
            (r, g, b) = colorsys.hsv_to_rgb(ii * 2 + self.wavePos, 1, 1)
            #self.leds.setColor(i, RGB(r, g, b))
            
            if (i < 90):
                self.leds.setColor(i, RGB(1,0,0))
            else:
                self.leds.setColor(i, RGB(0,0,1))