import tekore as tk
from pydantic import BaseSettings


class Settings(BaseSettings):
    # LED strip
    use_backend: str = "raspberrypi"  # "arduino" or "raspberrypi"
    led_count: int  # Number of LED pixels.
    led_brightness: float = 0.25  # in range between 0.0 and 1.0
    led_2d_coords: list[tuple[float, float]] = None  # Defaults to straight line
    # Raspberry Pi specific
    raspi_pin: int = 18  # GPIO pin connected to the pixels (18 uses PWM!, 10 uses SPI /dev/spidev0.0).
    raspi_freq_hz: int = 800000  # LED signal frequency in hertz (usually 800khz)
    raspi_dma: int = 10  # DMA channel to use for generating signal (try 10)
    raspi_invert: bool = False  # True to invert the signal (when using NPN transistor level shift)
    raspi_channel: int = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    # Arduino specific
    arduino_serial_header: list[int] = [42, 43, 44, 45, 46]
    arduino_serial_baudrate: int = 2000000
    arduino_serial_port: str = "/dev/ttyUSB0"
    # Spotify
    spotify_client_id: str
    spotify_redirect_uri: str
    spotify_scope: tk.scope = tk.scope.user_read_playback_state
    spotify_cache: str = "tekore.cfg"
    spotify_timeout: int = 15  # timeout (s) when calling the API
    spotify_update_interval: int = 10  # playback update interval (s)
    spotify_playback_offset_ms: int = 0  # offset for spotify callbacks

    class Config:
        env_file = ".env"


settings = Settings()
