from fastapi import APIRouter, Body

from . import strip

router = APIRouter(prefix="/strip")


@router.get("/num-pixels")
def num_pixels():
    return strip.num_pixels()


@router.get("/pixels")
def get_pixels():
    return strip.get_pixels()


@router.get("/brightness")
def get_brightness():
    return strip.get_brightness()


@router.post("/brightness")
def set_brightness(brightness: int = Body(ge=0, le=255)):
    strip.set_brightness(brightness)
