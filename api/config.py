import tekore as tk
from pydantic import BaseSettings


# fmt: off
class Settings(BaseSettings):
    # LED strip
    led_count: int  # Number of LED pixels.
    led_pin: int = 18  # GPIO pin connected to the pixels (18 uses PWM!, 10 uses SPI /dev/spidev0.0).
    led_freq_hz: int = 800000  # LED signal frequency in hertz (usually 800khz)
    led_dma: int = 10  # DMA channel to use for generating signal (try 10)
    led_brightness: float = 0.25  # in range between 0.0 and 1.0
    led_invert: bool = False # True to invert the signal (when using NPN transistor level shift)
    led_channel: int = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    # Spotify
    spotify_client_id: str
    spotify_redirect_uri: str
    spotify_scope: tk.scope = tk.scope.user_read_playback_state
    spotify_cache: str = "tekore.cfg"
    spotify_timeout: int = 15 # timeout (s) when calling the API

    class Config:
        env_file = ".env"
# fmt: on


settings = Settings()
