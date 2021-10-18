from app.visualizer.base_audio import BaseAudioVisualizer
from app.visualizer.spotify.philipp import PhilippsSpotifyVisualizer


class PhilippsAudioSpotifyVisualizer(BaseAudioVisualizer, PhilippsSpotifyVisualizer):
    def generic_callback(self, delta):
        super().generic_callback(delta)
        with self.lock:
            audio_filter = self.audio_filter
        if audio_filter:
            power = (1 + 9 * audio_filter.power()) / 10
            for i in range(self.leds.n_leds):
                self.leds.mul_color(i, power)


# TODO: cleanup does not work with multi inheritance
