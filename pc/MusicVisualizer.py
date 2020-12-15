from LightstripState import RGB
import math

def setRGB(colors, pos, color):
    if (pos > 0 and pos < len(colors)):
        colors[pos] = color

class MusicVisualizer:
    leds = None

    beat_num = 0
    segment_num = 0
    colA = RGB(255, 0, 0)
    colB = RGB(0, 0, 255)
    wavePos = 0
    brightness = 1
    isBeatActive = False

    def __init__(self, leds):
        self.leds = leds

    def sectionCallback(self, section):
        # Disable beat effect for sections without recognizable beat
        if (section["time_signature_confidence"] > 0.1):
            self.isBeatActive = True
        else:
            self.isBeatActive = False

        self.segment_num += 1
        if (self.segment_num % 2 == 0):
            self.colA = RGB(255, 0, 0)
            self.colB = RGB(0, 255, 0)
        else:
            self.colA = RGB(255, 0, 0)
            self.colB = RGB(0, 0, 255)
        print(section)

    def barCallback(self, bar):
        bar = bar

    def beatCallback(self, beat):
        self.beat_num += 1
        if (self.isBeatActive):
            colTmp = self.colA
            self.colA = self.colB
            self.colB = colTmp
        if (self.beat_num % 2 == 1):
            self.brightness = 1
        print(beat)

    def tatumCallback(self, tatum):
        self.tatum = tatum

    def segmentCallback(self, segment):
        segment = segment

    def genericCallback(self, delta):
        if (self.isBeatActive):
            self.brightness *= 0.98
        self.wavePos += delta

        # Calculate new colors
        for i in range(0, self.leds.num_leds):
            ii = i / self.leds.num_leds * math.pi
            self.leds.colors[i] = (self.colA * abs(math.sin(ii + self.wavePos)) + self.colB * abs(math.cos(ii + self.wavePos))) * self.brightness
