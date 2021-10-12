import threading
import time

from app.audio import AudioStream


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Visualizer:
    start_time = 0
    last_update = 0
    _visualizer = None
    thread = None

    def __init__(self, leds):
        self.leds = leds

    def start(self, visualizer):
        self._visualizer = visualizer
        self.start_time = time.time()
        self.last_update = self.start_time
        if self.thread == None:
            self.thread = StoppableThread(target=self.loop, args=[])
            self.thread.start()

    def end(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread.join()
            self.thread = None

    def loop(self):
        audio_stream = AudioStream()
        while not self.thread.stopped():
            now = time.time()
            delta = now - self.last_update
            self.last_update = now
            self.leds = self._visualizer.update(delta, self.leds)
            self.leds.show(audio_stream.read())
