import numpy as np
from pydantic import confloat

from ...spotify.shared_data import SharedData
from .sub import SingleSub


class ScaleLoudness(SingleSub):
    def __init__(self, config: "ScaleLoudness.Config") -> None:
        super().__init__(config)
        self.config: ScaleLoudness.Config
        self.scaling = 0
        self.loudness_interpolation = None

    class Config(SingleSub.Config):
        sensitivity: confloat(ge=0, le=10) = 6

    async def on_pause(self, shared_data: SharedData) -> None:
        await self.animation.on_pause(shared_data)
        self.loudness_interpolation = None

    async def on_resume(self, shared_data: SharedData) -> None:
        await self.animation.on_resume(shared_data)
        self.loudness_interpolation = (await shared_data.get_audio_analysis()).loudness_interpolation

    async def on_track_change(self, shared_data: SharedData) -> None:
        await self.animation.on_track_change(shared_data)
        self.loudness_interpolation = (await shared_data.get_audio_analysis()).loudness_interpolation

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        try:
            self.scaling = self.loudness_interpolation(progress)
        except (TypeError, ValueError):
            self.scaling *= 0.95  # fade out
        return super().render(progress, xy) * (self.scaling**self.config.sensitivity)

    def depends_on_spotify(self) -> bool:
        return True
