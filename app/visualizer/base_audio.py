from threading import RLock

import numpy as np
import pyaudio
from app.visualizer.base import BaseVisualizer
from apscheduler.schedulers.background import BackgroundScheduler
from scipy.signal import butter, filtfilt


class BaseAudioVisualizer(BaseVisualizer):
    def __init__(self, app):
        super().__init__(app)
        self.audio_stream = AudioStream()
        self.audio_filter = None
        self.lock = RLock()
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.read_stream)
        self.scheduler.start()

    def cleanup(self):
        self.scheduler.shutdown()
        return super().cleanup()

    def read_stream(self):
        while True:
            audio_filter = self.audio_stream.read()
            with self.lock:
                self.audio_filter = audio_filter


class AudioStream:
    def __init__(self):
        self.chunk = 256
        self.rate = 44100
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            frames_per_buffer=self.chunk,
            format=pyaudio.paInt16,
            channels=2,
            rate=self.rate,
            input=True,
        )

    def read(self):
        num_frames = max(self.audio_stream.get_read_available(), self.chunk)
        data = self.audio_stream.read(num_frames, exception_on_overflow=False)
        signal = np.frombuffer(data, dtype=np.int16).astype(np.float)
        return AudioFilter(signal, self.rate)

    def close(self):
        self.audio_stream.close()


class AudioFilter:
    power_normalizer = 2 ** 15

    def __init__(self, signal, rate):
        self.signal = signal
        self.rate = rate

    def power(self):
        return self._power(self.signal)

    def lowpass_power(self, cutoff=30):
        filtered_signal = AudioFilter._butter_highpass_filter(
            self.signal, cutoff, self.rate, order=5, btype="lowpass"
        )
        return self._power(filtered_signal)

    def highpass_power(self, cutoff=60):
        filtered_signal = AudioFilter._butter_highpass_filter(
            self.signal, cutoff, self.rate, order=5, btype="highpass"
        )
        return self._power(filtered_signal)

    def _power(self, signal):
        return min(np.sqrt(np.mean(signal ** 2)) / self.power_normalizer, 1.0)

    @staticmethod
    def _butter_highpass_filter(data, cutoff, fs, btype, order=5):
        b, a = AudioFilter._butter_highpass(cutoff, fs, order=order, btype=btype)
        y = filtfilt(b, a, data)
        return y

    @staticmethod
    def _butter_highpass(cutoff, fs, order, btype):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        return b, a
