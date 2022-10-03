import httpx
import tekore as tk

from .config import settings

_async_sender = tk.AsyncSender(client=httpx.AsyncClient(timeout=15))
_user_auth = None
_credentials = tk.Credentials(
    client_id=settings.spotify_client_id,
    redirect_uri=settings.spotify_redirect_uri,
    asynchronous=True,
    sender=_async_sender,
)
_spotify = tk.Spotify(asynchronous=True, sender=_async_sender)


def create_auth_url():
    global _user_auth
    _user_auth = tk.UserAuth(_credentials, settings.spotify_scope, pkce=True)
    return _user_auth.url


def wrap_token_refresh(coro):
    async def wrapped(*args, **kwargs):
        if _spotify.token is None:
            return None

        if _spotify.token.is_expiring:
            print("update token!")
            _spotify.token = await _credentials.refresh(_spotify.token)
            tk.config_to_file(
                settings.spotify_cache, (None, None, None, _spotify.token.refresh_token)
            )

        return await coro(*args, **kwargs)

    return wrapped


@wrap_token_refresh
async def current_user() -> tk.model.PrivateUser:
    return await _spotify.current_user()


@wrap_token_refresh
async def playback_currently_playing() -> tk.model.CurrentlyPlaying:
    return await _spotify.playback_currently_playing()


@wrap_token_refresh
async def track_audio_analysis(track_id) -> tk.model.AudioAnalysis:
    return await _spotify.track_audio_analysis(track_id)


async def load_token():
    try:
        _, _, _, refresh_token = tk.config_from_file(
            settings.spotify_cache, return_refresh=True
        )
        _spotify.token = await _credentials.refresh_pkce_token(refresh_token)
        tk.config_to_file(
            settings.spotify_cache, (None, None, None, _spotify.token.refresh_token)
        )
    except FileNotFoundError:
        pass


async def save_token(code: str, state: str):
    assert _user_auth is not None
    _spotify.token = await _user_auth.request_token(code, state)
    tk.config_to_file(
        settings.spotify_cache, (None, None, None, _spotify.token.refresh_token)
    )
