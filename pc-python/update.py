from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from analysis import AnalysisState
from threading import Thread
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

class VisualizationState:
    connection    = None
    colors        = None
    num_leds      = 0
    analysisState = None
    sectionCallback = None
    barCallback     = None
    beatCallback    = None
    tatumCallback   = None
    segmentCallback = None
    genericCallback = None
    lastUpdate       = None
    def __init__(self, device_path, num_leds, sectionCallback, barCallback, beatCallback, tatumCallback, segmentCallback, genericCallback):
        self.connection = Serial(device_path, 500000, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=None)
        self.colors = [RGB(0, 0, 0)] * num_leds
        self.num_leds = num_leds
        self.sectionCallback = sectionCallback
        self.barCallback = barCallback
        self.beatCallback = beatCallback
        self.tatumCallback = tatumCallback
        self.segmentCallback = segmentCallback
        self.genericCallback = genericCallback

    def startVisualization(self, data, elapsedSoFar):
        self.analysisState = AnalysisState(data, elapsedSoFar)
        self.lastUpdate = time.time()

    def endVisualization(self):
        self.analysisState = None

    def updateVisualization(self):
        now = time.time()
        self.analysisState.update(now - self.lastUpdate)
        if self.analysisState.sectionUpdate:
            self.sectionCallback(self, self.analysisState.data["sections"][self.analysisState.currSection])
        if self.analysisState.barUpdate:
            self.barCallback(self, self.analysisState.data["bars"][self.analysisState.currBar])
        if self.analysisState.beatUpdate:
            self.beatCallback(self, self.analysisState.data["beats"][self.analysisState.currBeat])
        if self.analysisState.tatumUpdate:
            self.tatumCallback(self, self.analysisState.data["tatums"][self.analysisState.currTatum])
        if self.analysisState.segmentUpdate:
            self.segmentCallback(self, self.analysisState.data["segments"][self.analysisState.currSegment])
        self.genericCallback(self, now - self.lastUpdate)
        self.lastUpdate = now
        # Put new data to LEDs
        self.connection.write(bytes([42, 43, 44, 45, 46]))
        for x in range(0, self.num_leds):
            self.connection.write(bytes([self.colors[x].g, self.colors[x].r, self.colors[x].b]))

thread = None

def loop(state):
    while True:
        state.updateVisualization()

def startUpdater(state, data, elapsedSoFar):
    global thread
    endUpdater()
    state.startVisualization(data, elapsedSoFar)
    thread = Thread(target = loop, args = [state])
    thread.start()
    #loop(state)

def endUpdater():
    global thread
    if thread is not None:
        thread._stop()
        thread = None
