from fastapi import APIRouter, Body
from pydantic import BaseModel, conint
from rpi_ws281x import Color

from ..animations import fill, rainbow, pride, theater, spotify_animation
from ..strip import strip


class ColorModel(BaseModel):
    red: conint(ge=0, le=255)
    green: conint(ge=0, le=255)
    blue: conint(ge=0, le=255)

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


@router.post("/fill")
async def start_fill(color_model: ColorModel):
    strip.start_animation(fill, color_model.get_color())


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    strip.start_animation(rainbow, delay)


@router.post("/pride")
async def start_pride():
    strip.start_animation(pride)


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    strip.start_animation(theater, delay)


@router.post("/spotify")
async def start_spotify(color_model: ColorModel):
    strip.start_animation(spotify_animation, color_model.red, color_model.green, color_model.blue)
