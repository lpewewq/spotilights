import asyncio
import time
from abc import ABC
from typing import List

import tekore as tk

from ..spotify import playback_currently_playing, track_audio_analysis
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

    def __init__(
        self, strip: "LEDStrip", update_interval=10, no_playback_sleep=10
    ) -> None:
        super().__init__(strip)
        self.update_interval = update_interval
        self.no_playback_sleep = no_playback_sleep
        self._fetch_time = 0.0
        self._currently_playing: tk.model.CurrentlyPlaying = None
        self._currently_playing_lock = asyncio.Lock()
        self._audio_analysis: tk.model.AudioAnalysis = None
        self._audio_analysis_lock = asyncio.Lock()

    def get_currently_playing(self):
        return self._currently_playing

    async def set_currently_playing(self, currently_playing):
        async with self._currently_playing_lock:
            self._currently_playing = currently_playing

    def get_audio_analysis(self):
        return self._audio_analysis

    async def set_audio_analysis(self, audio_analysis):
        async with self._audio_analysis_lock:
            self._audio_analysis = audio_analysis

    async def _update_playback(self, once=False):
        item_id = None
        while True:
            currently_playing = await playback_currently_playing()
            fetch_time = time.time()

            if (
                currently_playing is None
                or currently_playing.item.type != "track"
                or currently_playing.item.is_local
            ):
                await self.set_currently_playing(None)
                await self.set_audio_analysis(None)
            else:
                currently_playing.timestamp = int(fetch_time * 1000)
                await self.set_currently_playing(currently_playing)
                if currently_playing.item.id != item_id:
                    item_id = currently_playing.item.id
                    audio_analysis = await track_audio_analysis(
                        currently_playing.item.id
                    )
                    await self.set_audio_analysis(audio_analysis)
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
        try:
            while True:
                currently_playing = self.get_currently_playing()
                audio_analysis = self.get_audio_analysis()
                if currently_playing is None or audio_analysis is None:
                    await asyncio.sleep(self.no_playback_sleep)
                    continue

                if item_id != currently_playing.item.id:
                    await self.on_track_change(currently_playing, audio_analysis)
                    item_id = currently_playing.item.id
                    current_beat_index = None
                    current_section_index = None

                progress = currently_playing.progress_ms / 1000
                if currently_playing.is_playing:
                    progress += time.time() - currently_playing.timestamp / 1000

                beat_index = find(audio_analysis.beats, progress, current_beat_index)
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
        finally:
            update_playback_task.cancel()

    async def loop(self) -> None:
        pass

    async def on_track_change(
        self,
        currently_playing: tk.model.CurrentlyPlaying,
        audio_analysis: tk.model.AudioAnalysis,
    ) -> None:
        """Track change callback"""
        pass

    async def on_beat(self, beat: tk.model.TimeInterval) -> None:
        """Beat callback"""
        pass

    async def on_section(self, section: tk.model.TimeInterval) -> None:
        """Section callback"""
        pass
