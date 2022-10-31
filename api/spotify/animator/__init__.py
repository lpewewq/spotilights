from ...config import settings
from ...strip import strip
from ..client import spotify_client
from .animator import SpotifyAnimator
from .playback_state import SpotifyPlaybackState

spotify_state = SpotifyPlaybackState(
    spotify_client=spotify_client,
    offset_ms=settings.spotify_playback_offset_ms,
)

spotify_animator = SpotifyAnimator(
    spotify_state=spotify_state,
    strip=strip,
    update_interval=settings.spotify_update_interval,
)
