import asyncio
import time
from typing import List

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
            tk.config_to_file(settings.spotify_cache, (None, None, None, _spotify.token.refresh_token))

        return await coro(*args, **kwargs)

    return wrapped


@wrap_token_refresh
async def current_user():
    return await _spotify.current_user()


@wrap_token_refresh
async def playback_currently_playing():
    return await _spotify.playback_currently_playing()


@wrap_token_refresh
async def track_audio_analysis(track_id):
    return await _spotify.track_audio_analysis(track_id)


async def load_token():
    try:
        _, _, _, refresh_token = tk.config_from_file(settings.spotify_cache, return_refresh=True)
        _spotify.token = await _credentials.refresh_pkce_token(refresh_token)
        tk.config_to_file(settings.spotify_cache, (None, None, None, _spotify.token.refresh_token))
    except FileNotFoundError:
        pass


async def save_token(code: str, state: str):
    assert _user_auth is not None
    _spotify.token = await _user_auth.request_token(code, state)
    tk.config_to_file(settings.spotify_cache, (None, None, None, _spotify.token.refresh_token))


# class SharedData:
#     def __init__(self):
#         self.data = None
#         self.lock = asyncio.Lock()

#     async def get_data(self):
#         async with self.lock:
#             return self.data

#     async def set_data(self, data):
#         async with self.lock:
#             self.data = data


# async def update_playback(shared_playback, shared_analysis, update_interval=10):
#     item_id = None
#     while True:
#         playback = await playback_currently_playing()
#         fetch_time = time.time()

#         if playback is None or playback.item.type != "track" or playback.item.is_local:
#             await shared_playback.set_data(None)
#             await shared_analysis.set_data(None)
#             await asyncio.sleep(update_interval)
#             continue

#         await shared_playback.set_data((fetch_time, playback))
#         if playback.item.id != item_id:
#             item_id = playback.item.id
#             audio_analysis = await track_audio_analysis(playback.item.id)
#             await shared_analysis.set_data(audio_analysis)

#         await asyncio.sleep(update_interval)


# def find(list: List[tk.model.TimeInterval], timestamp, previous_index):
#     index = None
#     if previous_index is None:
#         for i, _beat in enumerate(list):
#             if _beat.start <= timestamp < _beat.start + _beat.duration:
#                 index = i
#                 break
#     elif list[previous_index].start <= timestamp:
#         for i, _beat in enumerate(list[previous_index:]):
#             if _beat.start <= timestamp < _beat.start + _beat.duration:
#                 index = previous_index + i
#                 break
#     else:
#         for i, _beat in enumerate(list[previous_index::-1]):
#             if _beat.start <= timestamp < _beat.start + _beat.duration:
#                 index = previous_index - i
#                 break
#     return index


# async def animation_loop(
#     shared_playback, 
#     shared_analysis, 
#     no_playback_sleep=10,
#     on_playback_change=lambda playback: None,
#     on_beat=lambda beat: None,
#     on_section=lambda section: None,
#     on_loop=lambda progress: None,
# ):
#     item_id = None
#     current_beat_index = None
#     current_section_index = None

#     while True:
#         playback: tk.model.CurrentlyPlaying = await shared_playback.get_data()
#         analysis: tk.model.AudioAnalysis = await shared_analysis.get_data()
#         if playback is None or analysis is None:
#             await asyncio.sleep(no_playback_sleep)
#             continue

#         fetch_time, playback = playback
#         if item_id != playback.item.id:
#             on_playback_change(playback, analysis)
#             item_id = playback.item.id
#             current_beat_index = None
#             current_section_index = None

#         progress = playback.progress_ms / 1000
#         if playback.is_playing:
#             progress += time.time() - fetch_time

#         beat_index = find(analysis.beats, progress, current_beat_index)
#         section_index = find(analysis.sections, progress, current_section_index)

#         if section_index and current_section_index != section_index:
#             current_section_index = section_index
#             on_section(analysis.sections[current_section_index])

#         if beat_index and current_beat_index != beat_index:
#             current_beat_index = beat_index
#             on_beat(analysis.beats[current_beat_index])

#         on_loop(progress)
#         await asyncio.sleep(0)
