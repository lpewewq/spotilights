import time
from abc import abstractmethod
from datetime import datetime
from threading import Lock

import spotipy
from app.visualizer.base import BaseVisualizer
from apscheduler.schedulers.background import BackgroundScheduler
from spotipy.oauth2 import SpotifyOAuth
from app.visualizer.spotify.analysis_provider import AnalysisProvider


class BaseSpotifyVisualizer(BaseVisualizer):
    def __init__(self, app):
        super().__init__(app)
        self.playback = None
        self.analysis_provider = None
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
                self.analysis_provider = None
            return

        # correct playback progress (ms -> s) and correction term for current_playback call
        new_playback["progress_ms"] = new_playback["progress_ms"] / 1000 + (time.time() - playback_update_time) / 2

        # update analysis of new item
        new_analysis = None
        new_item_id = new_playback["item"]["id"]
        if self.playback is None or self.playback["item"]["id"] != new_item_id:
            new_analysis = self.spotify.audio_analysis(new_item_id)

        # update playback and analysis
        with self.lock:
            self.playback = new_playback
            if new_analysis:
                self.analysis_provider = AnalysisProvider(new_analysis)

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
            playback_artist_info = ", ".join([a["name"] for a in self.playback["item"]["artists"]])
            playback_progress = int(self.playback["progress_ms"])
            playback_fps = int(1.0 / delta)
            print(
                f"[{playback_track_info} by {playback_artist_info}] Progress: {playback_progress}s FPS: {playback_fps} {' ' * 10}",
                end="\r",
            )

            if self.analysis_provider:
                time = self.playback["progress_ms"]
                current_section, has_changed = self.analysis_provider.get_current_section(time)
                if has_changed:
                    self.section_callback(current_section)
                current_bar, has_changed = self.analysis_provider.get_current_bar(time)
                if has_changed:
                    self.bar_callback(current_bar)
                current_beat, has_changed = self.analysis_provider.get_current_beat(time)
                if has_changed:
                    self.beat_callback(current_beat)
                current_tatum, has_changed = self.analysis_provider.get_current_tatum(time)
                if has_changed:
                    self.tatum_callback(current_tatum)
                current_segment, has_changed = self.analysis_provider.get_current_segment(time)
                if has_changed:
                    self.segment_callback(current_segment)

                self.generic_callback(delta)

                # trigger instant update if track ends
                if self.playback["progress_ms"] > self.analysis_provider.track.duration:
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
