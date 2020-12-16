import time
from LightstripState import LightstripState

class MusicPlaybackState:
    data           = None
    progress       = 0
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
    musicVisualizer = None
    endCallback    = None

    def __init__(self, data, secondsOffset, musicVisualizer, endCallback):
        self.data = data
        self.progress = secondsOffset
        self.lenSections = len(data["sections"])
        self.lenBars = len(data["bars"])
        self.lenBeats = len(data["beats"])
        self.lenTatums = len(data["tatums"])
        self.lenSegments = len(data["segments"])
        self.musicVisualizer = musicVisualizer
        self.endCallback = endCallback

    def callback(self, leds, delta):
        self.progress += delta
        #print(self.progress)
        while self.currSection < self.lenSections and self.data["sections"][self.currSection]["start"] <= self.progress:
            self.musicVisualizer.sectionCallback(self.data["sections"][self.currSection])
            self.currSection += 1
        while self.currBar < self.lenBars and self.data["bars"][self.currBar]["start"] <= self.progress:
            self.musicVisualizer.barCallback(self.data["bars"][self.currBar])
            self.currBar += 1
        while self.currBeat < self.lenBeats and self.data["beats"][self.currBeat]["start"] <= self.progress:
            self.musicVisualizer.beatCallback(self.data["beats"][self.currBeat])
            self.currBeat += 1
        while self.currTatum < self.lenTatums and self.data["tatums"][self.currTatum]["start"] <= self.progress:
            self.musicVisualizer.tatumCallback(self.data["tatums"][self.currTatum])
            self.currTatum += 1
        while self.currSegment < self.lenSegments and self.data["segments"][self.currSegment]["start"] <= self.progress:
            self.musicVisualizer.segmentCallback(self.data["segments"][self.currSegment])
            self.currSegment += 1
        self.musicVisualizer.genericCallback(leds, delta)

        if (self.currSection == self.lenSections):
            if (self.data["sections"][self.currSection - 1]["start"] + self.data["sections"][self.currSection - 1]["duration"] <= self.progress):
                self.endCallback()
