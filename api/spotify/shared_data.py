import asyncio

import tekore as tk


class SharedData:
    def __init__(self) -> None:
        self._currently_playing_lock = asyncio.Lock()
        self._currently_playing: tk.model.CurrentlyPlaying = None
        self._audio_analysis_lock = asyncio.Lock()
        self._audio_analysis: tk.model.AudioAnalysis = None

    async def get_currently_playing(self) -> tk.model.CurrentlyPlaying:
        async with self._currently_playing_lock:
            return self._currently_playing

    async def get_audio_analysis(self) -> tk.model.AudioAnalysis:
        async with self._audio_analysis_lock:
            return self._audio_analysis

    async def set_currently_playing(self, currently_playing: tk.model.CurrentlyPlaying) -> None:
        async with self._currently_playing_lock:
            self._currently_playing = currently_playing

    async def set_audio_analysis(self, audio_analysis: tk.model.AudioAnalysis) -> None:
        async with self._audio_analysis_lock:
            self._audio_analysis = audio_analysis
