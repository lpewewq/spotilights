from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from ..spotify import create_auth_url, current_user, load_token, save_token

router = APIRouter(prefix="/spotify")


@router.on_event("startup")
async def startup_load_token():
    await load_token()


@router.get("/current-user")
async def get_current_user():
    return await current_user()


@router.get("/oauth")
def oauth():
    return {"authorize_url": create_auth_url()}


@router.get("/oauth-callback")
async def callback(code: str, state: str):
    try:
        await save_token(code, state)
    except AssertionError:
        raise HTTPException(status_code=400)

    return RedirectResponse("/")
