from fastapi import APIRouter, Body
from pydantic import BaseModel, conint
from rpi_ws281x import Color, PixelStrip

from ..config import settings


class LEDStrip(PixelStrip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin()
        self.clear()

    def clear(self):
        self.fillColor(Color(0, 0, 0))
        self.show()

    def fillColor(self, color):
        for i in range(self.numPixels()):
            self.setPixelColor(i, color)


strip = LEDStrip(
    num=settings.led_count,
    pin=settings.led_pin,
    freq_hz=settings.led_freq_hz,
    dma=settings.led_dma,
    invert=settings.led_invert,
    brightness=settings.led_brightness,
    channel=settings.led_channel,
)


class ColorModel(BaseModel):
    red: conint(ge=0, le=255, strict=True)
    green: conint(ge=0, le=255, strict=True)
    blue: conint(ge=0, le=255, strict=True)

    def get_color(self):
        return Color(self.red, self.green, self.blue)


router = APIRouter(prefix="/strip")


@router.get("/num-pixels")
def num_pixels():
    return strip.numPixels()


@router.get("/pixels")
def get_pixels():
    return strip.getPixels()[:]


@router.get("/brightness")
def get_brightness():
    return strip.getBrightness()


@router.post("/brightness")
def set_brightness(brightness: int = Body(ge=0, le=255)):
    strip.setBrightness(brightness)
