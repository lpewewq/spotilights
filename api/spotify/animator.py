import asyncio
import time
import traceback
from typing import List

import tekore as tk

from ..animation.base import BaseAnimation
from ..strip import LEDStrip
from .updater import SpotifyUpdater


class SpotifyAnimator:
    def __init__(self, spotify_updater: SpotifyUpdater, strip: LEDStrip) -> None:
        self.spotify_updater = spotify_updater
        self.strip = strip
        self.animation_task: asyncio.Task = None

    async def start(self, animation_cls: type[BaseAnimation], *args, **kwargs) -> None:
        await self.spotify_updater.start()
        self.cancel_animation_task()
        animation = animation_cls(
            *args,
            **kwargs,
            strip=self.strip,
            shared_data=self.spotify_updater.shared_data,
        )
        self.animation_task = asyncio.create_task(self._loop(animation))

    def stop(self) -> None:
        self.cancel_animation_task()
        self.spotify_updater.stop()
        self.strip.clear()

    def cancel_animation_task(self) -> None:
        if self.animation_task is not None and not self.animation_task.done():
            self.animation_task.cancel()

    async def _loop(self, animation: BaseAnimation) -> None:
        current_segment_index = None
        current_tatum_index = None
        current_beat_index = None
        current_bar_index = None
        current_section_index = None
        item_id = None
        is_playing = True

        try:
            while True:
                currently_playing = (
                    await self.spotify_updater.shared_data.get_currently_playing()
                )
                audio_analysis = (
                    await self.spotify_updater.shared_data.get_audio_analysis()
                )
                if currently_playing and audio_analysis:
                    if item_id != currently_playing.item.id:
                        await animation.on_track_change()
                        item_id = currently_playing.item.id
                        current_segment_index = None
                        current_tatum_index = None
                        current_beat_index = None
                        current_bar_index = None
                        current_section_index = None

                    progress = currently_playing.progress_ms / 1000
                    if not currently_playing.is_playing:
                        if is_playing:
                            is_playing = False
                            await animation.on_pause()
                    else:
                        if not is_playing:
                            is_playing = True
                            await animation.on_resume()

                        progress += time.time() - currently_playing.timestamp / 1000

                        segment_index = self.find(
                            audio_analysis.segments, progress, current_segment_index
                        )
                        tatum_index = self.find(
                            audio_analysis.tatums, progress, current_tatum_index
                        )
                        beat_index = self.find(
                            audio_analysis.beats, progress, current_beat_index
                        )
                        bar_index = self.find(
                            audio_analysis.bars, progress, current_bar_index
                        )
                        section_index = self.find(
                            audio_analysis.sections, progress, current_section_index
                        )

                        if section_index and current_section_index != section_index:
                            current_section_index = section_index
                            section = audio_analysis.sections[current_section_index]
                            progress = (progress - section.start) / section.duration
                            await animation.on_section(section, progress)

                        if bar_index and current_bar_index != bar_index:
                            current_bar_index = bar_index
                            bar = audio_analysis.bars[current_bar_index]
                            progress = (progress - bar.start) / bar.duration
                            await animation.on_bar(bar, progress)

                        if beat_index and current_beat_index != beat_index:
                            current_beat_index = beat_index
                            beat = audio_analysis.beats[current_beat_index]
                            progress = (progress - beat.start) / beat.duration
                            await animation.on_beat(beat, progress)

                        if tatum_index and current_tatum_index != tatum_index:
                            current_tatum_index = tatum_index
                            tatum = audio_analysis.tatums[current_tatum_index]
                            progress = (progress - tatum.start) / tatum.duration
                            await animation.on_tatum(tatum, progress)

                        if segment_index and current_segment_index != segment_index:
                            current_segment_index = segment_index
                            segment = audio_analysis.segments[current_segment_index]
                            progress = (progress - segment.start) / segment.duration
                            await animation.on_segment(segment, progress)

                await animation.on_loop()
                await asyncio.sleep(0)

        except Exception as e:
            print(f"{animation} excepted:", e)
            traceback.print_exc()

    def find(self, list: List[tk.model.TimeInterval], timestamp, previous_index):
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
