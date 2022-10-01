from pydantic import BaseSettings


class Settings(BaseSettings):
    # LED strip
    led_count: int  # Number of LED pixels.
    led_pin: int = 18  # GPIO pin connected to the pixels (18 uses PWM!, 10 uses SPI /dev/spidev0.0).
    led_freq_hz: int = 800000  # LED signal frequency in hertz (usually 800khz)
    led_dma: int = 10  # DMA channel to use for generating signal (try 10)
    led_brightness: int = 64  # Set to 0 for darkest and 255 for brightest
    led_invert: bool = False  # True to invert the signal (when using NPN transistor level shift)
    led_channel: int = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    # Spotify
    spotify_client_id: str
    spotify_redirect_uri: str

    class Config:
        env_file = ".env"


settings = Settings()
