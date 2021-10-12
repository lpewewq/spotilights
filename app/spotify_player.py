import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from app.lightstrip_state import RGB
from app.music_visualizer import MusicVisualizer


class SpotifyVisualizer:
    playback = None
    playback_update_time = None
    playback_update_interval = 5

    def __init__(self, app, leds):
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=app.config["SPOTIPY_CLIENT_ID"],
                client_secret=app.config["SPOTIPY_CLIENT_SECRET"],
                scope=app.config["SPOTIPY_SCOPE"],
                redirect_uri=app.config["SPOTIPY_REDERICT_URI"],
            )
        )
        self.music_visualizer = MusicVisualizer(leds)

    def update(self, delta, leds):
        # update playback track and audio analysis
        if (
            self.playback_update_time is None
            or time.time() - self.playback_update_time > self.playback_update_interval
        ):
            self.playback_update_time = time.time()
            new_playback = self.spotify.current_playback()
            if new_playback is None:
                print("Playback unavailable.", end="\r")
                leds.clear()
                self.playback = None
                return leds
            # correct playback progress (ms -> s) and correction term for current_playback call
            new_playback["progress_ms"] = (
                new_playback["progress_ms"] / 1000
                + (time.time() - self.playback_update_time) / 2
            )

            # update analysis of new item
            new_item_id = new_playback["item"]["id"]
            if self.playback is None or self.playback["item"]["id"] != new_item_id:

                self.analysis = self.spotify.audio_analysis(new_item_id)
                self.curr_section = 0
                self.curr_bar = 0
                self.curr_beat = 0
                self.curr_tatum = 0
                self.curr_segment = 0

            # update playback
            self.playback = new_playback

        if self.playback is None or not self.playback["is_playing"]:
            leds.clear()
            return leds

        # update playback progress
        self.playback["progress_ms"] += delta

        # console logging
        playback_track_info = self.playback["item"]["name"]
        playback_artist_info = ", ".join(
            [a["name"] for a in self.playback["item"]["artists"]]
        )
        playback_progress = int(self.playback["progress_ms"])
        playback_fps = int(1.0 / delta)
        print(
            f"[{playback_track_info} by {playback_artist_info}] Progress: {playback_progress}s FPS: {playback_fps} {' ' * 10}",
            end="\r",
        )

        # visualizer callbacks
        def intersects(analysis_attr, curr_index):
            start = self.analysis[analysis_attr][curr_index]["start"]
            duration = self.analysis[analysis_attr][curr_index]["duration"]
            return start <= self.playback["progress_ms"] < start + duration

        if self.analysis:
            # calling the callback functions the dirty way
            for analysis_item in ["section", "bar", "beat", "tatum", "segment"]:
                self_attr = "curr_" + analysis_item
                analysis_attr = analysis_item + "s"
                attr_callback = analysis_item + "_callback"

                curr_index = getattr(self, self_attr)
                if (
                    self.analysis[analysis_attr][curr_index]["start"]
                    <= self.playback["progress_ms"]
                ):
                    # increment index to a newer item
                    while not intersects(
                        analysis_attr, curr_index
                    ) and curr_index + 1 < len(self.analysis[analysis_attr]):
                        curr_index += 1
                else:
                    # decrement index to a previous item
                    while (
                        not intersects(analysis_attr, curr_index)
                        and curr_index - 1 >= 0
                    ):
                        curr_index -= 1
                # check if index changed
                if curr_index != getattr(self, self_attr):
                    setattr(self, self_attr, curr_index)
                    getattr(self.music_visualizer, attr_callback)(
                        self.analysis[analysis_attr][curr_index]
                    )
            self.music_visualizer.generic_callback(delta)

            # trigger instant update if track ends
            if self.playback["progress_ms"] > self.analysis["track"]["duration"]:
                self.playback_update_time = None
        return leds
