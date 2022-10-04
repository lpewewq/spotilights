from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from . import spotify_client, spotify_animator

router = APIRouter(prefix="/spotify")


@router.on_event("shutdown")
def shutdown():
    spotify_animator.stop()


@router.on_event("startup")
async def startup_load_token():
    await spotify_client.load_token()


@router.get("/current-user")
async def get_current_user():
    return await spotify_client.current_user()


@router.get("/oauth")
def oauth():
    return {"authorize_url": spotify_client.create_auth_url()}


@router.get("/oauth-callback")
async def callback(code: str, state: str):
    try:
        await spotify_client.save_token(code, state)
    except AssertionError:
        raise HTTPException(status_code=400)

    return RedirectResponse("/")
