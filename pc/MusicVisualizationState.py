import time
from Lightstrip import LightstripState

class MusicVisualizationState:
    data           = None
    elapsedSeconds = 0
    currSection    = 0
    currBar        = 0
    currBeat       = 0
    currTatum      = 0
    currSegment    = 0
    lenSections    = 0
    lenBars        = 0
    lenBeats       = 0
    lenTatums      = 0
    lenSegments    = 0
    sectionUpdate  = False
    barUpdate      = False
    beatUpdate     = False
    tatumUpdate    = False
    segmentUpdate  = False
    sectionCallback = None
    barCallback     = None
    beatCallback    = None
    tatumCallback   = None
    segmentCallback = None
    genericCallback = None

    def __init__(self, data, secondsOffset, sectionCallback, barCallback, beatCallback, tatumCallback, segmentCallback, genericCallback):
        self.data = data
        self.elapsedSeconds = secondsOffset
        self.lenSections = len(data["sections"])
        self.lenBars = len(data["bars"])
        self.lenBeats = len(data["beats"])
        self.lenTatums = len(data["tatums"])
        self.lenSegments = len(data["segments"])
        self.sectionCallback = sectionCallback
        self.barCallback = barCallback
        self.beatCallback = beatCallback
        self.tatumCallback = tatumCallback
        self.segmentCallback = segmentCallback
        self.genericCallback = genericCallback

    def update(self, state, delta):
        newElapsed = state.lastUpdate - state.startTime

        while self.data["sections"][self.currSection]["start"] + self.data["sections"][self.currSection]["duration"] < newElapsed:
            self.currSection += 1
            self.sectionUpdate = True
        if self.sectionUpdate and self.currSection < self.lenSections:
            if self.data["sections"][self.currSection]["start"] + self.data["sections"][self.currSection]["duration"] >= newElapsed:
                self.sectionCallback(state, self.data["sections"][self.currSection])
                self.sectionUpdate = False

        while self.data["bars"][self.currBar]["start"] + self.data["bars"][self.currBar]["duration"] < newElapsed:
            self.currBar += 1
            self.barUpdate = True
        if self.barUpdate and self.currBar < self.lenBars:
            if self.data["bars"][self.currBar]["start"] + self.data["bars"][self.currBar]["duration"] >= newElapsed:
                self.barCallback(state, self.data["bars"][self.currBar])
                self.barUpdate = False
        
        while self.data["beats"][self.currBeat]["start"] + self.data["beats"][self.currBeat]["duration"] < newElapsed:
            self.currBeat += 1
            self.beatUpdate = True
        if self.beatUpdate and self.currBeat < self.lenBeats:
            if self.data["beats"][self.currBeat]["start"] + self.data["beats"][self.currBeat]["duration"] >= newElapsed:
                self.beatCallback(state, self.data["beats"][self.currBeat])
                self.beatUpdate = False

        while self.data["tatums"][self.currTatum]["start"] + self.data["tatums"][self.currTatum]["duration"] < newElapsed:
            self.currTatum += 1
            self.tatumUpdate = True
        if self.tatumUpdate and self.currTatum < self.lenTatums:
            if self.data["tatums"][self.currTatum]["start"] + self.data["tatums"][self.currTatum]["duration"] >= newElapsed:
                self.tatumCallback(state, self.data["tatums"][self.currTatum])
                self.tatumUpdate = False

        while self.data["segments"][self.currSegment]["start"] + self.data["segments"][self.currSegment]["duration"] < newElapsed:
            self.currSegment += 1
            self.segmentUpdate = True
        if self.segmentUpdate and self.currSegment < self.lenSegments:
            if self.data["segments"][self.currSegment]["start"] + self.data["segments"][self.currSegment]["duration"] >= newElapsed:
                self.segmentCallback(state, self.data["segments"][self.currSegment])
                self.segmentUpdate = False

        self.genericCallback(state, delta)
