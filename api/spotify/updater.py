import time

import tekore as tk

from .client import SpotifyClient
from .models import AudioAnalysis


def find(list, timestamp: float, previous_index: int) -> int:
    if previous_index is None:
        for i, item in enumerate(list):
            if item.start <= timestamp < item.start + item.duration:
                return i
    elif list[previous_index].start <= timestamp:
        for i, item in enumerate(list[previous_index:]):
            if item.start <= timestamp < item.start + item.duration:
                return previous_index + i
    else:
        for i, item in enumerate(list[previous_index::-1]):
            if item.start <= timestamp < item.start + item.duration:
                return previous_index - i
    return None


class SpotifyUpdater:
    def __init__(self, spotify_client: SpotifyClient, offset_ms: int = 0) -> None:
        self.spotify_client = spotify_client
        self.offset_ms = offset_ms
        self.clear()

    def clear(self) -> None:
        self.currently_playing: tk.model.CurrentlyPlaying = None
        self.audio_analysis: AudioAnalysis = None
        self.current_indices = [None, None, None, None, None]  # section, bar, beat, tatum, segment

    def duration_overflow(self, progress: float) -> bool:
        if self.currently_playing is None:
            return False
        return progress > (self.currently_playing.item.duration_ms / 1000)

    def progress(self) -> float:  # seconds
        if self.currently_playing is None:
            return 0

        if self.currently_playing.is_playing:
            return time.time() - self.currently_playing.timestamp / 1000
        else:
            return self.currently_playing.progress_ms / 1000

    def trigger_callbacks(self, progress: float, callbacks: list) -> None:
        if self.audio_analysis is None:
            return
        attribute_names = ["sections", "bars", "beats", "tatums", "segments"]
        for i in range(5):
            item_list = getattr(self.audio_analysis, attribute_names[i])
            index = find(item_list, progress, self.current_indices[i])
            if index and self.current_indices[i] != index:
                self.current_indices[i] = index
                callbacks[i](item_list[index], progress)

    async def update(self) -> bool:
        currently_playing: tk.model.CurrentlyPlaying = await self.spotify_client.playback_currently_playing()
        if (
            currently_playing is None
            or currently_playing.item is None
            or currently_playing.item.is_local
            or currently_playing.progress_ms is None
        ):
            self.clear()
            return False
        # Calculating the exact timing of the current playback
        # Related Issue: https://github.com/spotify/web-api/issues/1073
        # Workaround: Use provided timestamp as long as it is created at song start
        # If song is paused/resumed/seeked this timestamp needs to be corrected
        fetch_time_ms = int(time.time() * 1000)
        if currently_playing.timestamp > fetch_time_ms - currently_playing.progress_ms:
            currently_playing.timestamp = fetch_time_ms - currently_playing.progress_ms + self.offset_ms

        track_changed = self.currently_playing is None or currently_playing.item.id != self.currently_playing.item.id
        if track_changed:
            tk_audio_analysis = await self.spotify_client.track_audio_analysis(currently_playing.item.id)
            self.audio_analysis = AudioAnalysis.from_tekore(tk_audio_analysis)
            self.current_indices = [None, None, None, None, None]
        self.currently_playing = currently_playing
        return track_changed
