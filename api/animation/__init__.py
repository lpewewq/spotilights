import asyncio

from fastapi import APIRouter

from ..strip import LEDStrip, strip
from .base import BaseAnimation


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
router = APIRouter(prefix="/animation")


@router.on_event("shutdown")
def shutdown():
    animator.stop(clear=True)


from .fill import *
from .pride import *
from .rainbow import *
from .theater import *
