import numpy as np
from pydantic import Field, confloat

from ...spotify.models import AudioAnalysis
from .sub import SingleSub


class ScaleLoudness(SingleSub):
    def __init__(self, config: "ScaleLoudness.Config") -> None:
        super().__init__(config)
        self.config: ScaleLoudness.Config
        self.scaling = 0
        self.loudness_interpolation = None

    class Config(SingleSub.Config):
        sensitivity: confloat(ge=0, le=10, multiple_of=0.1) = Field(
            6, config_type="Numerical", title="Sensitivity", description=" "
        )

        @property
        def needs_spotify(self) -> bool:
            return True

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        self.animation.on_track_change(analysis)
        self.loudness_interpolation = analysis.loudness_interpolation

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        try:
            self.scaling = self.loudness_interpolation(progress)
        except (TypeError, ValueError):
            self.scaling *= 0.95  # fade out
        return super().render(progress, xy) * (self.scaling**self.config.sensitivity)
