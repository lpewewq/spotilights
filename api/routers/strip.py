from fastapi import APIRouter, Body
from pydantic import BaseModel, condecimal
from rpi_ws281x import Color

from ..scheduler import to_byte, fill, rainbow, pride, theater
from ..strip import strip


class ColorModel(BaseModel):
    red: condecimal(ge=0.0, le=1.0)
    green: condecimal(ge=0.0, le=1.0)
    blue: condecimal(ge=0.0, le=1.0)

    def get_color(self):
        r = to_byte(self.red)
        g = to_byte(self.green)
        b = to_byte(self.blue)
        return Color(r, g, b)


router = APIRouter(prefix="/strip")


@router.on_event("shutdown")
def shutdown():
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
