import threading
import time

class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class Visualizer:
    leds           = None
    startTime      = 0
    lastUpdate     = 0
    updateCallback = None
    thread         = None

    def __init__(self, leds, updateCallback):
        self.leds = leds
        self.updateCallback = updateCallback

    def startVisualization(self):
        self.thread = StoppableThread(target = self.loop, args = [])
        self.startTime = time.time()
        self.lastUpdate = self.startTime
        self.thread.start()

    def endVisualization(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread.join()
            self.thread = None
    
    def loop(self):
        while not self.thread.stopped():
            now = time.time()
            delta = now - self.lastUpdate
            self.lastUpdate = now
            self.updateCallback(delta)
            self.leds.show()
