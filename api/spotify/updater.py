import asyncio
import time
import traceback

from .client import SpotifyClient
from .shared_data import SharedData


class SpotifyUpdater:
    def __init__(self, spotify_client: SpotifyClient, update_interval: int, offset_ms: int = 0) -> None:
        self.spotify_client = spotify_client
        self.update_interval = update_interval
        self.offset_ms = offset_ms
        self.update_task: asyncio.Task = None
        self.shared_data = SharedData()

    def start(self) -> None:
        if self.update_task is None or self.update_task.done():
            self.update_task = asyncio.create_task(self._loop())

    def stop(self) -> None:
        if self.update_task is not None and not self.update_task.done():
            self.update_task.cancel()

    async def _loop(self) -> None:
        item_id = None
        try:
            while True:
                currently_playing = await self.spotify_client.playback_currently_playing()
                fetch_time = time.time()

                if currently_playing is None or currently_playing.item is None or currently_playing.item.is_local:
                    await self.shared_data.set_currently_playing(None)
                    await self.shared_data.set_audio_analysis(None)
                else:
                    currently_playing.timestamp = int(fetch_time * 1000) + self.offset_ms
                    if currently_playing.item.id != item_id:
                        item_id = currently_playing.item.id
                        audio_analysis = await self.spotify_client.track_audio_analysis(currently_playing.item.id)
                        await self.shared_data.set_audio_analysis(audio_analysis)
                    await self.shared_data.set_currently_playing(currently_playing)
                await asyncio.sleep(self.update_interval)
        except Exception as e:
            print(f"SpotifyUpdater excepted:", e)
            traceback.print_exc()
