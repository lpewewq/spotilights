from ..config import settings
from .client import SpotifyClient

spotify_client = SpotifyClient(
    client_id=settings.spotify_client_id,
    redirect_uri=settings.spotify_redirect_uri,
    scope=settings.spotify_scope,
    cache_file=settings.spotify_cache,
    timeout=settings.spotify_timeout,
)
