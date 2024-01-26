from pathlib import Path

import numpy as np
import tekore as tk
from pydantic import BaseSettings, validator
from enum import Enum


class StripBackend(str, Enum):
    raspberrypi = "raspberrypi"
    arduino = "arduino"


class Settings(BaseSettings):
    # LED strip
    use_backend: StripBackend
    led_count: int  # Number of LED pixels.
    led_brightness: float = 0.25  # in range between 0.0 and 1.0
    led_2d_coords: list[tuple[float, float]] = None  # Defaults to straight line
    animation_data_path: Path = Path("animation_data")
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
    spotify_cache: Path = Path("tekore.cfg")
    spotify_timeout: int = 15  # timeout (s) when calling the API
    spotify_update_interval: int = 10  # playback update interval (s)
    spotify_playback_offset_ms: int = 0  # offset for spotify callbacks
    # Finetuning
    segment_loudness_resample_rate: int = 60
    segment_loudness_smoothing_kernel_size: float = 1  # gaussian kernel window size in seconds

    @validator("led_2d_coords")
    def led_2d_coords_validator(cls, v, values):
        n = values.get("led_count")
        if v:
            if len(v) != n:
                raise ValueError("number of 2D coordinates mismatch led count")
            v = np.array(v)
        else:
            v = np.linspace([-1, 0], [1, 0], n)
        # normalize to unit circle
        centered = v - (v.max(axis=0) + v.min(axis=0)) / 2
        normalized = centered / np.max(np.linalg.norm(centered, axis=1))
        return normalized

    class Config:
        env_file = ".env"


settings = Settings()
