import random

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from ..config import settings
from ..spotify import get_spotify, spotify_auth_manager

router = APIRouter(prefix="/spotify")


@router.get("/me")
def index():
    if spotify_auth_manager.get_cached_token() is None:
        return None

    return get_spotify().me()


@router.get("/currently-playing")
def index():
    if spotify_auth_manager.get_cached_token() is None:
        return None

    return get_spotify().currently_playing()


@router.get("/oauth")
def oauth():
    return {
        "authorize_url": spotify_auth_manager.get_authorize_url()
    }


@router.get("/oauth-callback")
def callback(code: str, state: int):
    if state != spotify_auth_manager.state:
        raise HTTPException(status_code=401)

    spotify_auth_manager.state = random.randint(1, 10e10)
    spotify_auth_manager.get_access_token(code, check_cache=False)
    return RedirectResponse("/")
