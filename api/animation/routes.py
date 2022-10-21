from fastapi import APIRouter, Body

from ..color import IntColorModel
from ..spotify import spotify_animator
from .base import Mirror
from .basic import Fill, Wave2D
from .complex import PhilippsAnimation
from .spotifyless import Pride, Rainbow, Theater

router = APIRouter(prefix="/animation")


@router.post("/fill")
async def start_fill(color: IntColorModel, low: float = Body(ge=0, le=1)):
    animation = Fill(color.get_color(), low=low)
    spotify_animator.start(animation)


@router.post("/wave")
async def start_2d_wave(color: IntColorModel, low: float = Body(0.5, ge=0, le=1), fineness: float = Body(10, ge=1, le=100)):
    animation = Wave2D(color.get_color(), low=low, fineness=fineness)
    spotify_animator.start(animation)


@router.post("/philipp")
async def start_philipp():
    animation = PhilippsAnimation()
    spotify_animator.start(animation)


@router.post("/pride")
async def start_pride():
    animation = Pride()
    spotify_animator.start(animation)


@router.post("/rainbow")
async def start_rainbow(delay: float = Body(0.5, ge=0)):
    animation = Mirror(Rainbow(delay), divisions=4)
    spotify_animator.start(animation)


@router.post("/theater")
async def start_theater(delay: float = Body(0.05, ge=0)):
    animation = Mirror(Theater(delay), divisions=2, inverse=[True, False])
    spotify_animator.start(animation)
