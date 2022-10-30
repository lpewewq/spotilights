import asyncio
import time

from ..animation import AnimationModel
from ..strip.abstract import AbstractStrip
from .updater import SpotifyUpdater


class SpotifyAnimator:
    def __init__(self, spotify_updater: SpotifyUpdater, strip: AbstractStrip, update_interval: int) -> None:
        self.spotify_updater = spotify_updater
        self.strip = strip
        self.update_interval = update_interval
        self.animation_loop: asyncio.Task = None

    def start(self, animation_model: AnimationModel) -> None:
        if self.animation_loop is not None and not self.animation_loop.done():
            self.animation_loop.cancel()
        self.animation_loop = asyncio.create_task(self.animate(animation_model))

    async def animate(self, animation_model: AnimationModel) -> None:
        needs_spotify = animation_model.config.needs_spotify
        animation = animation_model.construct()
        callbacks = [
            animation.on_section,
            animation.on_bar,
            animation.on_beat,
            animation.on_tatum,
            animation.on_segment,
        ]

        loop_count = 0
        loop_start = time.time()
        next_spotify_update = loop_start
        while True:
            loop_count += 1
            now = time.time()
            if needs_spotify:
                progress = self.spotify_updater.progress()
                if now > next_spotify_update or self.spotify_updater.duration_overflow(progress):
                    track_changed = await self.spotify_updater.update()
                    next_spotify_update = now + self.update_interval
                    if track_changed:
                        animation.on_track_change(self.spotify_updater.audio_analysis)
                self.spotify_updater.trigger_callbacks(progress, callbacks)
                colors = animation.render(progress, self.strip.xy)
            else:
                progress = now - loop_start
                colors = animation.render(progress, self.strip.xy)

            self.strip.show(colors)
            await asyncio.sleep(0)

            if loop_count % 10 == 0:
                now = time.time()
                print(f"FPS: {10 / (now - loop_start):.02f}, Progress: {progress:.02f}s".ljust(50), end="\r")
                loop_start = now

    def stop(self) -> None:
        if self.animation_loop is not None and not self.animation_loop.done():
            self.animation_loop.cancel()
        self.strip.clear()
