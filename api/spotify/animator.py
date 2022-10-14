import asyncio
import time
import traceback

import tekore as tk

from ..animation.base import Animation
from ..strip.base import GlobalStrip
from .updater import SpotifyUpdater


class SpotifyAnimator:
    def __init__(self, spotify_updater: SpotifyUpdater, strip: GlobalStrip) -> None:
        self.spotify_updater = spotify_updater
        self.strip = strip
        self.animation_task: asyncio.Task = None

    def start(self, animation: Animation) -> None:
        if animation.depends_on_spotify:
            self.spotify_updater.start()
        else:
            self.spotify_updater.stop()
        self.cancel_animation_task()
        self.animation_task = asyncio.create_task(self._loop(animation))

    def stop(self) -> None:
        self.cancel_animation_task()
        self.spotify_updater.stop()
        self.strip.clear()
        self.strip.show()

    def cancel_animation_task(self) -> None:
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()

    async def _loop(self, animation: Animation) -> None:
        item_id = None
        # section, bar, beat, tatum, segment
        current_indices = [None, None, None, None, None]
        attribute_names = ["sections", "bars", "beats", "tatums", "segments"]
        callbacks = [animation.on_section, animation.on_bar, animation.on_beat, animation.on_tatum, animation.on_segment]

        is_playing = True
        loop_start = time.time()
        loop_count = 0

        try:
            while True:
                progress = time.time() - loop_start

                currently_playing = await self.spotify_updater.shared_data.get_currently_playing()
                audio_analysis = await self.spotify_updater.shared_data.get_audio_analysis()
                if currently_playing and audio_analysis:
                    if item_id != currently_playing.item.id:
                        await animation.on_track_change(self.spotify_updater.shared_data)
                        item_id = currently_playing.item.id
                        current_indices = [None, None, None, None, None]

                    if not currently_playing.is_playing or currently_playing.progress_ms is None:
                        if is_playing:
                            is_playing = False
                            await animation.on_pause(self.spotify_updater.shared_data)
                    else:
                        if not is_playing:
                            is_playing = True
                            await animation.on_resume(self.spotify_updater.shared_data)

                        progress = currently_playing.progress_ms / 1000
                        progress += time.time() - currently_playing.timestamp / 1000

                        for i in range(5):
                            item_list = getattr(audio_analysis, attribute_names[i])
                            callback = callbacks[i]
                            current_index = current_indices[i]
                            index = self.find(item_list, progress, current_index)
                            if index and current_index != index:
                                current_indices[i] = index
                                item = item_list[index]
                                await callback(item, progress)

                await animation.render(self.strip, progress)
                self.strip.show()
                await asyncio.sleep(0)
                loop_count += 1
                if loop_count % 60 == 0:
                    now = time.time()
                    print("FPS:", 60 / (now - loop_start), end="\r")
                    loop_start = now

        except Exception as e:
            print(f"{animation} excepted:", e)
            traceback.print_exc()

    def find(self, list, timestamp: float, previous_index: int) -> int:
        if previous_index is None:
            for i, _beat in enumerate(list):
                if _beat.start <= timestamp < _beat.start + _beat.duration:
                    return i
        elif list[previous_index].start <= timestamp:
            for i, _beat in enumerate(list[previous_index:]):
                if _beat.start <= timestamp < _beat.start + _beat.duration:
                    return previous_index + i
        else:
            for i, _beat in enumerate(list[previous_index::-1]):
                if _beat.start <= timestamp < _beat.start + _beat.duration:
                    return previous_index - i
        return None
