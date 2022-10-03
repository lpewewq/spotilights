import asyncio

from fastapi import APIRouter, Body
from pydantic import BaseModel, conint
from rpi_ws281x import Color

from ..animation.base import BaseAnimation
from ..animation.fill import FillAnimation
from ..animation.pride import PrideAnimation
from ..animation.rainbow import RainbowAnimation, TheaterAnimation
from ..routers.strip import LEDStrip, strip


class Animator:
    def __init__(self, strip: LEDStrip) -> None:
        self.strip: LEDStrip = strip
        self.animation_task: asyncio.Task = None

    def stop(self, clear=False) -> None:
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()
        if clear:
            self.strip.clear()

    def start(self, animation_cls: type[BaseAnimation], *args) -> None:
        self.stop()
        animation = animation_cls(self.strip, *args)
        self.animation_task = asyncio.create_task(animation.start())


animator = Animator(strip)


class ColorModel(BaseModel):
    red: conint(ge=0, le=255, strict=True)
    green: conint(ge=0, le=255, strict=True)
    blue: conint(ge=0, le=255, strict=True)

    def get_color(self):
        return Color(self.red, self.green, self.blue)


router = APIRouter(prefix="/animation")


@router.on_event("shutdown")
def shutdown():
    animator.stop(clear=True)


@router.post("/pride")
async def start_pride():
    animator.start(PrideAnimation)


@router.post("/fill")
async def start_fill(color_model: ColorModel):
    animator.start(FillAnimation, color_model)


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0.0)):
    animator.start(RainbowAnimation, delay)


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0.0)):
    animator.start(TheaterAnimation, delay)
