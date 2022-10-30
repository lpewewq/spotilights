import asyncio
import time

from ..animation import Animation, AnimationModel
from ..strip.abstract import AbstractStrip
from .updater import SpotifyUpdater


class SpotifyAnimator:
    def __init__(self, spotify_updater: SpotifyUpdater, strip: AbstractStrip) -> None:
        self.spotify_updater = spotify_updater
        self.strip = strip
        self.animation: Animation = None
        self.animation_loop: asyncio.Task = None
        # loop state
        self.item_id = None
        self.current_indices = [None, None, None, None, None]  # section, bar, beat, tatum, segment
        self.loop_start = time.time()
        self.loop_count = 0

    async def start(self, animation_model: AnimationModel) -> None:
        if animation_model.config.needs_spotify:
            self.spotify_updater.start()
        else:
            await self.spotify_updater.stop()

        if self.animation is None or not isinstance(self.animation, animation_model.animation):
            self.animation = animation_model.construct()
        else:
            self.animation.update_config(animation_model.config)
        self.item_id = None  # trigger on_track_change
        if self.animation_loop is None:
            self.animation_loop = asyncio.create_task(self.loop())

    async def stop(self) -> None:
        if self.animation_loop is not None and not self.animation_loop.done():
            self.animation_loop.cancel()
            self.animation_loop = None
        await self.spotify_updater.stop()
        self.strip.clear()

    async def loop(self) -> None:

        while True:
            progress = time.time() - self.loop_start

            currently_playing = await self.spotify_updater.shared_data.get_currently_playing()
            audio_analysis = await self.spotify_updater.shared_data.get_audio_analysis()
            if currently_playing and audio_analysis:
                if self.item_id != currently_playing.item.id:
                    await self.animation.on_track_change(self.spotify_updater.shared_data)
                    self.item_id = currently_playing.item.id
                    self.current_indices = [None, None, None, None, None]

                if not currently_playing.is_playing:
                    progress = currently_playing.progress_ms / 1000
                else:
                    progress = time.time() - currently_playing.timestamp / 1000

                    attribute_names = ["sections", "bars", "beats", "tatums", "segments"]
                    callbacks = [
                        self.animation.on_section,
                        self.animation.on_bar,
                        self.animation.on_beat,
                        self.animation.on_tatum,
                        self.animation.on_segment,
                    ]
                    for i in range(5):
                        item_list = getattr(audio_analysis, attribute_names[i])
                        callback = callbacks[i]
                        current_index = self.current_indices[i]
                        index = self.find(item_list, progress, current_index)
                        if index and current_index != index:
                            self.current_indices[i] = index
                            item = item_list[index]
                            callback(item, progress)

            colors = self.animation.render(progress, self.strip.xy)
            self.strip.show(colors)
            await asyncio.sleep(0)
            self.loop_count += 1
            if self.loop_count % 10 == 0:
                now = time.time()
                print(f"FPS: {10 / (now - self.loop_start):.02f}, Progress: {progress:.02f}s".ljust(50), end="\r")
                self.loop_start = now

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
