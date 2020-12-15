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

    def __init__(self, data, secondsOffset, musicVisualizer):
        self.data = data
        self.progress = secondsOffset
        self.lenSections = len(data["sections"])
        self.lenBars = len(data["bars"])
        self.lenBeats = len(data["beats"])
        self.lenTatums = len(data["tatums"])
        self.lenSegments = len(data["segments"])
        self.musicVisualizer = musicVisualizer

    def callback(self, delta):
        self.progress += delta
        while self.data["sections"][self.currSection]["start"] < self.progress and self.currSection < self.lenSections:
            self.currSection += 1
            self.musicVisualizer.sectionCallback(self.data["sections"][self.currSection])
        while self.data["bars"][self.currBar]["start"] < self.progress and self.currBar < self.lenBars:
            self.currBar += 1
            self.musicVisualizer.barCallback(self.data["bars"][self.currBar])
        while self.data["beats"][self.currBeat]["start"] + self.data["beats"][self.currBeat]["duration"] < self.progress and self.currBeat < self.lenBeats:
            self.currBeat += 1
            self.musicVisualizer.beatCallback(self.data["beats"][self.currBeat])
        while self.data["tatums"][self.currTatum]["start"] + self.data["tatums"][self.currTatum]["duration"] < self.progress and self.currTatum < self.lenTatums:
            self.currTatum += 1
            self.musicVisualizer.tatumCallback(self.data["tatums"][self.currTatum])
        while self.data["segments"][self.currSegment]["start"] + self.data["segments"][self.currSegment]["duration"] < self.progress and self.currSegment < self.lenSegments:
            self.currSegment += 1
            self.musicVisualizer.segmentCallback(self.data["segments"][self.currSegment])
        self.musicVisualizer.genericCallback(delta)
