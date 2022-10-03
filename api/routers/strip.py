import asyncio

from fastapi import APIRouter, Body
from pydantic import BaseModel, conint
from rpi_ws281x import Color, PixelStrip

from ..animation.base import BaseAnimation
from ..animation.pride import PrideAnimation
from ..animation.fill import FillAnimation
from ..animation.rainbow import RainbowAnimation, TheaterAnimation
from ..config import settings


async def animation_loop(animation: BaseAnimation):
    try:
        while True:
            await animation.loop()
            await asyncio.sleep(0)
    except Exception as e:
        print(f"{animation} excepted:", e)


class LEDStrip(PixelStrip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin()
        self.animation_task = None
        self.fillColor(Color(0, 0, 0))
        self.show()

    def stop_animation(self):
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()

    def start_animation(self, animation_cls: type[BaseAnimation], *args):
        self.stop_animation()
        animation = animation_cls(self, *args)
        self.animation_task = asyncio.create_task(animation_loop(animation))

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


@router.on_event("shutdown")
def shutdown():
    strip.stop_animation()
    strip.fillColor(Color(0, 0, 0))
    strip.show()


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


@router.post("/pride")
async def start_pride():
    strip.start_animation(PrideAnimation)

@router.post("/fill")
async def start_fill(color_model: ColorModel):
    strip.start_animation(FillAnimation, color_model.get_color())


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    strip.start_animation(RainbowAnimation, delay)


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    strip.start_animation(TheaterAnimation, delay)
