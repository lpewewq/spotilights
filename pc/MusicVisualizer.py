from LightstripState import RGB
import math

def setRGB(colors, pos, color):
    if (pos > 0 and pos < len(colors)):
        colors[pos] = color

class Comet:
    color = RGB(0, 0, 0)
    position = 0
    velocity = 0
    length = 40
    leds = None

    def __init__(self, leds, duration, color):
        self.color = color
        self.leds = leds
        self.velocity = (leds.num_leds / 2) / duration

    def show(self, delta):
        self.position += self.velocity * delta
        for i in range(0, self.length):
            if (self.position + i <= self.leds.num_leds / 2):
                self.leds.addColor(self.position - i, self.color * pow(i / self.length, 2))
                self.leds.addColor(self.leds.num_leds - (self.position - i), self.color * pow(i / self.length, 2))

class MusicVisualizer:
    leds = None

    beat_num = 0
    beatProgress = 0
    beatDuration = 1
    segment_num = 0

    isBeatActive = False
    fourOnTheFloor = False

    # Wave
    colA = RGB(1, 0, 0)
    colB = RGB(0, 0, 1)
    brightness = 1
    wavePos = 0
    waveVel = 0

    # Orb
    currLoudness = 0
    orbCol   = RGB(1, 1, 1)

    # Comets
    comets = []

    def __init__(self, leds):
        self.leds = leds

    def sectionCallback(self, section):
        # Disable beat effect for sections without recognizable beat
        if (section["time_signature_confidence"] > 0.1):
            self.isBeatActive = True
            if (section["time_signature"] == 4):
                self.fourOnTheFloor = True
            else:
                self.fourOnTheFloor = False
        else:
            self.isBeatActive = False
            self.fourOnTheFloor = False

        self.segment_num += 1
        if (self.segment_num % 2 == 0):
            self.colA = RGB(1, 0, 0)
            self.colB = RGB(0, 1, 0)
        else:
            self.colA = RGB(1, 0, 0)
            self.colB = RGB(0, 0, 1)
        print(section)

    def barCallback(self, bar):
        bar = bar

    def beatCallback(self, beat):
        self.beat_num += 1

        if (self.isBeatActive):
            self.wavePos += math.pi / 2
            if (self.beat_num % 2 == 1):
                self.beatProgress = 0
                self.beatDuration = beat["duration"] * 2
                self.comets.append(Comet(self.leds, beat["duration"], RGB(1, 1, 1)))
                self.brightness = 0
                if (len(self.comets) > 3):
                    self.comets.remove(self.comets[0])
        print(beat)

    def tatumCallback(self, tatum):
        self.tatum = tatum

    def segmentCallback(self, segment):
        self.currLoudness = segment["loudness_max"]
        #print(segment)

    def genericCallback(self, leds, delta):
        self.beatProgress += delta
        if (self.fourOnTheFloor):
            self.brightness *= 0.98
        #self.wavePos += delta * self.waveVel

        a = self.colA.lerp(self.colB, 1 - self.beatProgress / self.beatDuration)
        b = self.colB.lerp(self.colA, self.beatProgress / self.beatDuration)

        leds.fill(RGB(1, 1, 1) * 1)
        #for comet in self.comets:
            #comet.show(delta)

        orbWidth = int((1 - self.beatProgress / self.beatDuration) * 90)
        for i in range(0, orbWidth):
            self.leds.addColor(leds.num_leds / 2 + i, self.orbCol * pow((orbWidth - i) / orbWidth, 2))
            self.leds.addColor(self.leds.num_leds - (leds.num_leds / 2 + i), self.orbCol * pow((orbWidth - i) / orbWidth, 2))
        #self.leds.invert()

        # Calculate new colors
        for i in range(0, leds.num_leds):
            ii = i / leds.num_leds * math.pi / 2
            leds.mulColor(i, a * abs(math.sin(ii + self.wavePos)) + b * abs(math.cos(ii + self.wavePos)))

        
