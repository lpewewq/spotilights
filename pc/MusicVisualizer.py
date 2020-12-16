from LightstripState import RGB
from LightstripState import lerp
import math
import random

def getBell(x):
    return 1 / pow(1 + pow(x, 2), 3 / 2)

class MusicVisualizer:
    leds = None
    mode = 0
    numModes = 2

    sectionNum = 0

    barNum = 0
    barProgress = 0
    barDuration = 1

    beatNum = 0
    beatProgress = 0
    beatDuration = 1
    beatPairProgress = 0
    beatPairDuration = 1

    segmentNum = 0
    segmentProgress = 1
    segmentDuration = 1
    segmentLoudnessMaxTime = 1
    segmentLoudnessStart = 1
    segmentLoudnessMax = 1
    segmentLoudnessEnd = 1

    isBeatActive = False
    fourOnTheFloor = False

    # Wave
    colA = RGB(1, 0, 0)
    colB = RGB(0, 1, 0)
    colC = RGB(0, 0, 1)
    brightness = 1
    wavePos = 0
    waveVel = 1
    waveFreq = 1

    def __init__(self, leds):
        self.leds = leds

    def swapCols(self):
        colTmp = self.colA
        self.colA = self.colB
        self.colB = colTmp

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

        self.sectionLoudness = section["loudness"]
        self.waveVel = section["tempo"] / 100
        self.waveFreq = 1

        # Center color again
        self.wavePos = 0
        self.waveFreq = 1

        # Change colors
        choice = random.randint(0, 2)
        if choice == 0:
            self.colA = RGB(1, 0, 0)
            self.colB = RGB(0, 1, 0)
        if choice == 1:
            self.colA = RGB(1, 0, 0)
            self.colB = RGB(0, 0, 1)
        if choice == 2:
            self.colA = RGB(0.1, 1, 0)
            self.colB = RGB(0, 0, 1)
            self.colC = RGB(1, 0, 0)
        if choice == 3:
            self.colA = RGB(1, 0, 0)
            self.colB = RGB(1, 1, 0)
        wavePos = 0

        self.sectionNum += 1
        self.mode += 1
        self.mode %= self.numModes
        print(section)

    def barCallback(self, bar):
        self.barNum += 1
        self.barDuration = bar["duration"]
        self.barProgress = 0

    def beatCallback(self, beat):
        self.beatNum += 1
        self.beatProgress = 0
        self.beatDuration = beat["duration"]
        if self.beatNum % 2 == 1:
            self.brightness = 1
            self.beatPairProgress = 0
            self.beatPairDuration = self.beatDuration * 2

        if (self.isBeatActive and self.sectionNum % 3 == 0):
            self.swapCols()
        if (self.isBeatActive and self.sectionNum % 3 == 2):
            if self.beatNum % 2 == 1:
                self.swapCols()

        print(beat)

    def tatumCallback(self, tatum):
        if (self.isBeatActive and self.sectionNum % 3 == 1):
            self.swapCols()

    def segmentCallback(self, segment):
        self.segmentNum += 1
        self.segmentProgress = 0
        self.segmentDuration = segment["duration"]
        self.segmentLoudnessStart = segment["loudness_start"]
        self.segmentLoudnessMax = segment["loudness_max"]
        self.segmentLoudnessEnd = segment["loudness_end"]
        self.segmentLoudnessMaxTime = segment["loudness_max_time"]

    time = 0
    def genericCallback(self, leds, delta):
        self.time += delta
        self.beatProgress += delta
        self.beatPairProgress += delta
        self.segmentProgress += delta
        self.barProgress += delta
        
        cA = self.colA
        cB = self.colB

        center = leds.num_leds / 2
        beatProc = (self.beatProgress / self.beatDuration)
        beatPairProc = (self.beatPairProgress / self.beatPairDuration)
        barProc = self.barProgress / self.barDuration

        numModes = 3
        #self.sectionNum = 2
        if self.sectionNum % numModes == 0:
            leds.fill(RGB(0.1, 0.1, 0.1))
            if self.barNum % 16 < 14:
                if self.barNum % 8 < 4:
                    cycleProc = beatPairProc
                else:
                    cycleProc = 1 - beatPairProc
            else:
                cycleProc = (self.beatNum % 8) / 8
            for i in range(0, leds.num_leds):
                if (i > center):
                    leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - center - cycleProc * center) / 10, 2), 3 / 2)))
                    leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - center - (cycleProc + 1) * center) / 10, 2), 3 / 2)))
                else:
                    leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - center + cycleProc * center) / 10, 2), 3 / 2)))
                    leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - center + (cycleProc + 1) * center) / 10, 2), 3 / 2)))

        # Only looks good with time_signature=4
        if self.sectionNum % numModes == 1:
            if self.beatNum % 2 == 1:
                proc = beatProc
            else:
                proc = 0
            for i in range(0, int(leds.num_leds / 2) + 1):
                leds.setColor(i, RGB(1, 1, 1) * (1 - proc)
                    * pow(getBell((i - center + proc * center) / 10), 2))
                leds.setColor(leds.num_leds - i, leds.colors[i])

        if self.sectionNum % numModes == 2:
            self.waveFreq = 2
            self.wavePos += delta
            self.brightness *= 0.975
            for i in range(0, leds.num_leds):
                ii = i / leds.num_leds
                leds.setColor(i, RGB(1, 1, 1) * pow(math.sin(ii * math.pi), 2))     # Mask edges
                leds.mulColor(i, RGB(1, 1, 1) * self.brightness)

        for i in range(0, leds.num_leds):
            ii = ((i - leds.num_leds / 2) / leds.num_leds) * math.pi * self.waveFreq
            leds.mulColor(i, cA * abs(math.sin(ii + self.wavePos)) + cB * abs(math.cos(ii + self.wavePos)))

        
