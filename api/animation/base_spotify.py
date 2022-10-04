import asyncio
import time
import traceback
from abc import ABC, abstractmethod
from typing import List

import tekore as tk

from ..spotify import spotify_client
from ..strip.base import LEDStrip
from .base import BaseAnimation


def find(list: List[tk.model.TimeInterval], timestamp, previous_index):
    index = None
    if previous_index is None:
        for i, _beat in enumerate(list):
            if _beat.start <= timestamp < _beat.start + _beat.duration:
                index = i
                break
    elif list[previous_index].start <= timestamp:
        for i, _beat in enumerate(list[previous_index:]):
            if _beat.start <= timestamp < _beat.start + _beat.duration:
                index = previous_index + i
                break
    else:
        for i, _beat in enumerate(list[previous_index::-1]):
            if _beat.start <= timestamp < _beat.start + _beat.duration:
                index = previous_index - i
                break
    return index


class BaseSpotifyAnimation(BaseAnimation, ABC):
    """Interface for animations using the Spotify API."""

    def __init__(self, strip: LEDStrip, update_interval=10) -> None:
        super().__init__(strip)
        self.update_interval = update_interval
        self._fetch_time = 0.0
        # shared data
        self._shared_lock = asyncio.Lock()
        self._currently_playing: tk.model.CurrentlyPlaying = None
        self._audio_analysis: tk.model.AudioAnalysis = None

    async def get_currently_playing(self):
        async with self._shared_lock:
            return self._currently_playing

    async def get_audio_analysis(self):
        async with self._shared_lock:
            return self._audio_analysis

    async def _update_playback(self, once=False):
        item_id = None
        while True:
            currently_playing = await spotify_client.playback_currently_playing()
            fetch_time = time.time()

            if (
                currently_playing is None
                or currently_playing.item.type != "track"
                or currently_playing.item.is_local
            ):
                async with self._shared_lock:
                    self._currently_playing = None
                    self._audio_analysis = None
            else:
                currently_playing.timestamp = int(fetch_time * 1000)
                if currently_playing.item.id != item_id:
                    item_id = currently_playing.item.id
                    audio_analysis = await spotify_client.track_audio_analysis(
                        currently_playing.item.id
                    )
                    async with self._shared_lock:
                        self._currently_playing = currently_playing
                        self._audio_analysis = audio_analysis
                else:
                    async with self._shared_lock:
                        self._currently_playing = currently_playing
            if once:
                break
            else:
                await asyncio.sleep(self.update_interval)

    async def start(self) -> None:
        await self._update_playback(once=True)
        update_playback_task = asyncio.create_task(self._update_playback())

        current_beat_index = None
        current_section_index = None
        item_id = None
        is_playing = True

        try:
            while True:
                currently_playing = await self.get_currently_playing()
                audio_analysis = await self.get_audio_analysis()
                if currently_playing and audio_analysis:
                    if item_id != currently_playing.item.id:
                        await self.on_track_change()
                        item_id = currently_playing.item.id
                        current_beat_index = None
                        current_section_index = None

                    progress = currently_playing.progress_ms / 1000
                    if not currently_playing.is_playing:
                        if is_playing:
                            is_playing = False
                            await self.on_pause()
                    else:
                        if not is_playing:
                            is_playing = True
                            await self.on_resume()

                        progress += time.time() - currently_playing.timestamp / 1000

                        beat_index = find(
                            audio_analysis.beats, progress, current_beat_index
                        )
                        section_index = find(
                            audio_analysis.sections, progress, current_section_index
                        )

                        if section_index and current_section_index != section_index:
                            current_section_index = section_index
                            await self.on_section(
                                audio_analysis.sections[current_section_index]
                            )

                        if beat_index and current_beat_index != beat_index:
                            current_beat_index = beat_index
                            await self.on_beat(audio_analysis.beats[current_beat_index])

                await self.loop()
                await asyncio.sleep(0)

        except Exception as e:
            print(f"{self} excepted:", e)
            traceback.print_exc()
        finally:
            update_playback_task.cancel()

    @abstractmethod
    async def on_pause(self) -> None:
        """Playback paused callback"""

    @abstractmethod
    async def on_resume(self) -> None:
        """Playback resumed callback"""

    @abstractmethod
    async def on_track_change(self) -> None:
        """Track change callback"""

    @abstractmethod
    async def on_section(self, section: tk.model.TimeInterval) -> None:
        """Section callback"""

    @abstractmethod
    async def on_beat(self, beat: tk.model.TimeInterval) -> None:
        """Beat callback"""
