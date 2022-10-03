import warnings

import httpx
import tekore as tk


warnings.filterwarnings(
    "ignore", message="`SPOTIFY_CLIENT_ID` missing! None returned instead."
)
warnings.filterwarnings(
    "ignore", message="`SPOTIFY_CLIENT_SECRET` missing! None returned instead."
)
warnings.filterwarnings(
    "ignore", message="`SPOTIFY_REDIRECT_URI` missing! None returned instead."
)


def wrap_token_refresh(coro):
    async def wrapped(self, *args, **kwargs):
        if self._spotify.token is None:
            return None

        if self._spotify.token.is_expiring:
            print("update token!")
            self._spotify.token = await self._credentials.refresh(self._spotify.token)
            tk.config_to_file(
                self.cache_file, (None, None, None, self._spotify.token.refresh_token)
            )

        return await coro(self, *args, **kwargs)

    return wrapped


class SpotifyClient:
    def __init__(self, client_id, redirect_uri, scope, cache_file, timeout):
        _async_sender = tk.AsyncSender(client=httpx.AsyncClient(timeout=timeout))
        self.scope = scope
        self.cache_file = cache_file
        self._user_auth = None
        self._credentials = tk.Credentials(
            client_id=client_id,
            redirect_uri=redirect_uri,
            asynchronous=True,
            sender=_async_sender,
        )
        self._spotify = tk.Spotify(asynchronous=True, sender=_async_sender)

    async def load_token(self):
        try:
            _, _, _, refresh_token = tk.config_from_file(
                self.cache_file, return_refresh=True
            )
            self._spotify.token = await self._credentials.refresh_pkce_token(
                refresh_token
            )
            tk.config_to_file(
                self.cache_file, (None, None, None, self._spotify.token.refresh_token)
            )
        except FileNotFoundError:
            pass

    async def save_token(self, code: str, state: str):
        assert self._user_auth is not None
        self._spotify.token = await self._user_auth.request_token(code, state)
        tk.config_to_file(
            self.cache_file, (None, None, None, self._spotify.token.refresh_token)
        )

    def create_auth_url(self):
        self._user_auth = tk.UserAuth(self._credentials, self.scope, pkce=True)
        return self._user_auth.url

    @wrap_token_refresh
    async def current_user(self) -> tk.model.PrivateUser:
        return await self._spotify.current_user()

    @wrap_token_refresh
    async def playback_currently_playing(self) -> tk.model.CurrentlyPlaying:
        return await self._spotify.playback_currently_playing()

    @wrap_token_refresh
    async def track_audio_analysis(self, track_id) -> tk.model.AudioAnalysis:
        return await self._spotify.track_audio_analysis(track_id)
