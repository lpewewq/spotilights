import tekore as tk
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from ..config import settings

file = "tekore.cfg"
current_user_auth = None
scope = tk.scope.user_read_playback_state
cred = tk.Credentials(client_id=settings.spotify_client_id, redirect_uri=settings.spotify_redirect_uri, asynchronous=True)
spotify = tk.Spotify(asynchronous=True)


router = APIRouter(prefix="/spotify")


@router.on_event("startup")
async def update_token():
    try:
        conf = tk.config_from_file(file, return_refresh=True)
        spotify.token = await cred.refresh_pkce_token(conf[3])
        tk.config_to_file(file, (None, None, None, spotify.token.refresh_token))
    except FileNotFoundError:
        print("config not found")


@router.get("/current-user")
async def current_user():
    if spotify.token is None:
        return None

    if spotify.token.is_expiring:
        print("Token expired, update!")
        spotify.token = cred.refresh(spotify.token)
        tk.config_to_file(file, (None, None, None, spotify.token.refresh_token))

    return await spotify.current_user()


@router.get("/oauth")
def oauth():
    global current_user_auth
    current_user_auth = tk.UserAuth(cred, scope, pkce=True)
    return {"authorize_url": current_user_auth.url}


@router.get("/oauth-callback")
async def callback(code: str, state: str):
    if current_user_auth is None:
        raise HTTPException(status_code=400)

    try:
        spotify.token = await current_user_auth.request_token(code, state)
        tk.config_to_file(file, (None, None, None, spotify.token.refresh_token))
    except AssertionError:
        raise HTTPException(status_code=400)

    return RedirectResponse("/")
