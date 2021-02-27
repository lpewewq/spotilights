from LightstripState import RGB
from LightstripState import lerp
import math
import random

def getBell(x):
    return 1 / pow(1 + pow(x, 2), 3 / 2)

class State:
    leds = None
    time = 0
    sectionNum = 0
    sectionBars = 0
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

    def __init__(self, leds):
        self.leds = leds

class MusicVisualizer:
    state = None
    center = 0

    # Wave
    colA = RGB(1, 0, 0)
    colB = RGB(0, 1, 0)
    colC = RGB(0, 0, 1)
    brightness = None
    wavePos = 0
    waveVel = 1
    waveFreq = 1

    def __init__(self, leds):
        self.state = State(leds)
        self.center = self.state.leds.numLEDs / 2
        self.brightness = [RGB(1, 1, 1)] * self.state.leds.numLEDs

    def swapCols(self):
        colTmp = self.colA
        self.colA = self.colB
        self.colB = colTmp
        colTmp = self.colC
        self.colC = self.colD
        self.colD = colTmp

    def sectionCallback(self, section):
        self.state.sectionLoudness = section["loudness"]
        self.waveVel = section["tempo"] / 100
        self.waveFreq = 1

        # Center color again
        self.wavePos = 0
        self.waveFreq = 1

        # Start with first bar
        self.state.barNum = 0

        # Change colors
        choice = random.randint(0, 3)
        if choice == 0:
            self.colC = RGB(1, 0, 0)
            self.colD = RGB(0, 1, 0)
        if choice == 1:
            self.colC = RGB(1, 0, 0)
            self.colD = RGB(0, 0, 1)
        if choice == 2:
            self.colC = RGB(0.1, 1, 0)
            self.colD = RGB(0, 0, 1)
        if choice == 3:
            self.colC = RGB(1, 0, 0)
            self.colD = RGB(1, 1, 0)
        wavePos = 0

        self.state.sectionNum += 1
        print(section)

    def barCallback(self, bar):
        self.state.barNum += 1
        self.state.barDuration = bar["duration"]
        self.state.barProgress = 0

    def beatCallback(self, beat):
        self.state.beatNum += 1
        self.state.beatProgress = 0
        self.state.beatDuration = beat["duration"]

        self.swapCols()

        if self.state.sectionNum % 4 != 3:
            if self.state.beatNum % 2 == 1:
                self.brightness = [RGB(1, 1, 1)] * self.state.leds.numLEDs
                self.state.beatPairProgress = 0
                self.state.beatPairDuration = self.state.beatDuration * 2

        if self.state.sectionNum % 4 == 3:
            for i in range(0, self.state.leds.numLEDs):
                self.brightness[i] += RGB(1, 1, 1) * getBell((i - ((self.state.beatNum % 5) / 4) * 180) / 10)

        print(beat)

    def tatumCallback(self, tatum):
        tatum = tatum

    def segmentCallback(self, segment):
        self.state.segmentNum += 1
        self.state.segmentProgress = 0
        self.state.segmentDuration = segment["duration"]
        self.state.segmentLoudnessStart = segment["loudness_start"]
        self.state.segmentLoudnessMax = segment["loudness_max"]
        self.state.segmentLoudnessEnd = segment["loudness_end"]
        self.state.segmentLoudnessMaxTime = segment["loudness_max_time"]

    def genericCallback(self, delta):
        self.state.time += delta
        self.state.beatProgress += delta
        self.state.beatPairProgress += delta
        self.state.segmentProgress += delta
        self.state.barProgress += delta

        # Lerp colors in first bar of section (todo: lerp in HSV, not in RGB)
        if (self.state.barNum == 0):
            cA = self.colA.lerp(self.colC, 0)
            cB = self.colB.lerp(self.colD, 0)
        if (self.state.barNum == 1):
            cA = self.colA.lerp(self.colC, self.state.barProgress / self.state.barDuration)
            cB = self.colB.lerp(self.colD, self.state.barProgress / self.state.barDuration)
        if (self.state.barNum > 1):
            self.colA = self.colC
            self.colB = self.colD
            cA = self.colA
            cB = self.colB

        beatProc = (self.state.beatProgress / self.state.beatDuration)
        beatPairProc = (self.state.beatPairProgress / self.state.beatPairDuration)
        barProc = self.state.barProgress / self.state.barDuration

        numModes = 4
        #self.sectionNum = 2
        if self.state.sectionNum % numModes == 0:
            self.state.leds.fill(RGB(0.1, 0.1, 0.1))
            if self.state.beatNum % 32 < 24:
                if self.state.barNum % 6 < 3:
                    cycleProc = beatPairProc
                else:
                    cycleProc = 1 - beatPairProc
            else:
                cycleProc = (self.state.beatNum % 8) / 8
            for i in range(0, self.state.leds.numLEDs):
                if (i > self.center):
                    self.state.leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - self.center - cycleProc * self.center) / 10, 2), 3 / 2)))
                    self.state.leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - self.center - (cycleProc + 1) * self.center) / 10, 2), 3 / 2)))
                else:
                    self.state.leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - self.center + cycleProc * self.center) / 10, 2), 3 / 2)))
                    self.state.leds.addColor(i, RGB(1, 1, 1)
                        * (1 / pow(1 + pow((i - self.center + (cycleProc + 1) * self.center) / 10, 2), 3 / 2)))

        # Only looks good with time_signature=4
        if self.state.sectionNum % numModes == 1:
            for i in range(0, self.state.leds.numLEDs):
                self.brightness[i] *= 0.96
            self.waveFreq = 2
            self.wavePos += self.waveVel * (delta / 2)
            if self.state.beatNum % 4 < 2:
                proc = beatPairProc
            else:
                proc = (1 - beatPairProc)
            for i in range(0, int(self.state.leds.numLEDs / 2) + 1):
                ii = i / self.state.leds.numLEDs
                self.state.leds.setColor(i, RGB(1, 1, 1) * self.brightness[i] * pow(math.sin(ii * math.pi), 3)) # Mask edges
                self.state.leds.addColor(i, RGB(1, 1, 1) * (1 - proc)
                    * pow(getBell((i - self.center + proc * self.center) / 10), 2))
                self.state.leds.setColor(self.state.leds.numLEDs - i, self.state.leds.colors[i])

        if self.state.sectionNum % numModes == 2:
            self.waveFreq = 2
            self.wavePos += self.waveVel * delta
            for i in range(0, self.state.leds.numLEDs):
                self.brightness[i] *= 0.975
            for i in range(0, self.state.leds.numLEDs):
                ii = i / self.state.leds.numLEDs
                self.state.leds.setColor(i, self.brightness[i] * pow(math.sin(ii * math.pi), 2)) # Mask edges

        if self.state.sectionNum % numModes == 3:
            for i in range(0, self.state.leds.numLEDs):
                self.brightness[i] *= 0.96
            for i in range(0, self.state.leds.numLEDs):
                self.state.leds.setColor(i, self.brightness[i])

        for i in range(0, self.state.leds.numLEDs):
            ii = ((i - self.state.leds.numLEDs / 2) / self.state.leds.numLEDs) * math.pi * self.waveFreq
            self.state.leds.mulColor(i, cA * abs(math.sin(ii + self.wavePos)) + cB * abs(math.cos(ii + self.wavePos)))
