import random

from spotipy import Spotify, SpotifyPKCE

from .config import settings

spotify_auth_manager = SpotifyPKCE(
    client_id=settings.spotify_client_id,
    redirect_uri=settings.spotify_redirect_uri,
    scope=settings.spotify_scope,
    state=random.randint(1, 10e10),
    open_browser=False,
)


def get_spotify():
    return Spotify(auth_manager=spotify_auth_manager)
