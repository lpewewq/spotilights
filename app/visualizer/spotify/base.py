import time
from abc import abstractmethod
from datetime import datetime
from threading import Lock

import spotipy
from app.visualizer.base import BaseVisualizer
from apscheduler.schedulers.background import BackgroundScheduler
from spotipy.oauth2 import SpotifyOAuth


class BaseSpotifyVisualizer(BaseVisualizer):
    def __init__(self, app):
        super().__init__(app)
        self.playback = None
        self.analysis = None
        self.curr_section = 0
        self.curr_bar = 0
        self.curr_beat = 0
        self.curr_tatum = 0
        self.curr_segment = 0
        self.lock = Lock()

        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=app.config["SPOTIPY_CLIENT_ID"],
                client_secret=app.config["SPOTIPY_CLIENT_SECRET"],
                scope=app.config["SPOTIPY_SCOPE"],
                redirect_uri=app.config["SPOTIPY_REDERICT_URI"],
            )
        )

        self.scheduler = BackgroundScheduler()
        self.playback_update_job = self.scheduler.add_job(
            self.playback_update,
            "interval",
            seconds=app.config["SPOTIPY_PLAYBACK_UPDATE_INTERVAL"],
            next_run_time=datetime.now(),
        )
        self.scheduler.start()

    def cleanup(self):
        self.scheduler.shutdown()
        return super().cleanup()

    def playback_update(self):
        # update playback track and audio analysis
        playback_update_time = time.time()
        new_playback = self.spotify.current_playback()

        if new_playback is None:
            with self.lock:
                self.playback = None
                self.analysis = None
            return

        # correct playback progress (ms -> s) and correction term for current_playback call
        new_playback["progress_ms"] = (
            new_playback["progress_ms"] / 1000
            + (time.time() - playback_update_time) / 2
        )

        # update analysis of new item
        new_analysis = None
        new_item_id = new_playback["item"]["id"]
        if self.playback is None or self.playback["item"]["id"] != new_item_id:
            new_analysis = self.spotify.audio_analysis(new_item_id)

        # update playback and analysis
        with self.lock:
            self.playback = new_playback
            if new_analysis:
                self.analysis = new_analysis
                self.curr_section = 0
                self.curr_bar = 0
                self.curr_beat = 0
                self.curr_tatum = 0
                self.curr_segment = 0

    def update(self, delta):
        with self.lock:
            # clear if playback is paused or nonexistent
            if self.playback is None or not self.playback["is_playing"]:
                self.leds.clear()
                return self.leds

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
                        getattr(self, attr_callback)(
                            self.analysis[analysis_attr][curr_index]
                        )
                self.generic_callback(delta)

                # trigger instant update if track ends
                if self.playback["progress_ms"] > self.analysis["track"]["duration"]:
                    self.playback_update_job.modify(next_run_time=datetime.now())
                    self.playback = None
            return self.leds

    @abstractmethod
    def section_callback(self, section):
        pass

    @abstractmethod
    def bar_callback(self, bar):
        pass

    @abstractmethod
    def beat_callback(self, beat):
        pass

    @abstractmethod
    def tatum_callback(self, tatum):
        pass

    @abstractmethod
    def segment_callback(self, segment):
        pass

    @abstractmethod
    def generic_callback(self, delta):
        pass
