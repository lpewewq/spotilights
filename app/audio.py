import numpy as np
import pyaudio
from scipy.signal import butter, filtfilt


class AudioStream:
    rate = 44100

    def __init__(self):
        self.chunk = 256
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            frames_per_buffer=self.chunk,
            format=pyaudio.paInt16,
            channels=2,
            rate=self.rate,
            input=True,
        )

    def read(self):
        data = self.audio_stream.read(self.chunk, exception_on_overflow=False)
        signal = np.frombuffer(data, dtype=np.int16).astype(np.float)
        self.audio_stream.read(
            self.audio_stream.get_read_available(), exception_on_overflow=False
        )
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
