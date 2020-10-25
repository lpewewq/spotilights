class AnalysisState:
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

    def __init__(self, data, secondsOffset):
        self.data = data
        self.elapsedSeconds = secondsOffset
        self.lenSections = len(data["sections"])
        self.lenBars = len(data["bars"])
        self.lenBeats = len(data["beats"])
        self.lenTatums = len(data["tatums"])
        self.lenSegments = len(data["segments"])

    def update(self, delta):
        newElapsed = self.elapsedSeconds + delta
        self.sectionUpdate  = False
        self.barUpdate      = False
        self.beatUpdate     = False
        self.tatumUpdate    = False
        self.segmentUpdate  = False

        if self.currSection + 1 < self.lenSections:
            while self.data["sections"][self.currSection]["start"] + self.data["sections"][self.currSection]["duration"] < newElapsed:
                self.currSection += 1
                self.sectionUpdate = True

        if self.currBar + 1 < self.lenBars:      
            while self.data["bars"][self.currBar]["start"] + self.data["bars"][self.currBar]["duration"] < newElapsed:
                self.currBar += 1
                self.barUpdate = True

        if self.currBeat + 1 < self.lenBeats:
            while self.data["beats"][self.currBeat]["start"] + self.data["beats"][self.currBeat]["duration"] < newElapsed:
                self.currBeat += 1
                if self.data["beats"][self.currBeat]["start"] + self.data["beats"][self.currBeat]["duration"] >= newElapsed:
                    self.beatUpdate = True

        if self.currTatum + 1 < self.lenTatums:
            while self.data["tatums"][self.currTatum]["start"] + self.data["tatums"][self.currTatum]["duration"] < newElapsed:
                self.currTatum += 1
                self.tatumUpdate = True
        
        if self.currSegment + 1 < self.lenSegments:
            while self.data["segments"][self.currSegment]["start"] + self.data["segments"][self.currSegment]["duration"] < newElapsed:
                self.currSegment += 1
                self.segmentUpdate = True

        self.elapsedSeconds = newElapsed
