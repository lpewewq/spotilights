import asyncio
import time

from ...animation import Animation, AnimationModel
from ...strip.abstract import AbstractStrip
from .playback_state import SpotifyPlaybackState


class SpotifyAnimator:
    def __init__(self, spotify_state: SpotifyPlaybackState, strip: AbstractStrip, update_interval: int) -> None:
        self.spotify_state = spotify_state
        self.strip = strip
        self.update_interval = update_interval
        self.animation_task: asyncio.Task = None
        self.update_task: asyncio.Task = None
        self.animation: Animation = None

    def start(self, animation_model: AnimationModel) -> None:
        if self.animation is None or not isinstance(self.animation, animation_model.animation):
            self.animation = animation_model.construct()
            animation_changed = True
        else:
            animation_changed = self.animation.update_config(animation_model.config)

        if animation_changed and self.spotify_state.audio_analysis is not None:
            self.animation.on_track_change(self.spotify_state.audio_analysis)

        if self.animation_task is None:
            self.animation_task = asyncio.create_task(self.animate())

    def stop(self) -> None:
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()
            self.animation_task = None
        self.strip.clear()

    async def animate(self) -> None:
        loop_count = 0
        loop_start = time.time()
        next_spotify_update = loop_start
        while True:
            loop_count += 1
            now = time.time()

            if self.animation.config.needs_spotify:
                progress = self.spotify_state.progress()

                # check for playback update
                if self.update_task is None:
                    if now > next_spotify_update or self.spotify_state.duration_overflow(progress):
                        self.update_task = asyncio.create_task(self.spotify_state.update())

                # handle event callbacks
                self.spotify_state.trigger_callbacks(
                    progress,
                    [
                        self.animation.on_section,
                        self.animation.on_bar,
                        self.animation.on_beat,
                        self.animation.on_tatum,
                        self.animation.on_segment,
                    ],
                )

                # render animation
                colors = self.animation.render(progress, self.strip.xy)
            else:
                # spotifyless animation
                progress = now - loop_start
                colors = self.animation.render(progress, self.strip.xy)

            # draw animation to strip
            self.strip.show(colors)

            # prevent blocking
            await asyncio.sleep(0)

            # handle pending update task
            if self.update_task is not None and self.update_task.done():
                next_spotify_update = now + self.update_interval
                track_changed = self.update_task.result()
                self.update_task = None
                # handle track changed event
                if track_changed and self.animation.config.needs_spotify:
                    self.animation.on_track_change(self.spotify_state.audio_analysis)

            # stats
            if loop_count % 30 == 0:
                now = time.time()
                print(f"Progress: {progress:.02f}s, {30 / (now - loop_start):.02f} FPS".ljust(50), end="\r")
                loop_start = now
