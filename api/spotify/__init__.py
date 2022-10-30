from ..config import settings
from ..strip import strip
from .animator import SpotifyAnimator
from .client import SpotifyClient
from .updater import SpotifyUpdater

spotify_client = SpotifyClient(
    client_id=settings.spotify_client_id,
    redirect_uri=settings.spotify_redirect_uri,
    scope=settings.spotify_scope,
    cache_file=settings.spotify_cache,
    timeout=settings.spotify_timeout,
)

spotify_updater = SpotifyUpdater(
    spotify_client=spotify_client,
    offset_ms=settings.spotify_playback_offset_ms,
)

spotify_animator = SpotifyAnimator(
    spotify_updater=spotify_updater,
    strip=strip,
    update_interval=settings.spotify_update_interval,
    xy=settings.led_2d_coords,
)
