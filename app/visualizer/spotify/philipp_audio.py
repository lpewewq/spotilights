from app.visualizer.base_audio import BaseAudioVisualizer
from app.visualizer.spotify.philipp import PhilippsSpotifyVisualizer


class PhilippsAudioSpotifyVisualizer(BaseAudioVisualizer, PhilippsSpotifyVisualizer):
    def generic_callback(self, delta):
        super().generic_callback(delta)
        with self.lock:
            audio_filter = self.audio_filter
        power = (1 + 9 * audio_filter.power()) / 10
        return self.leds * power
