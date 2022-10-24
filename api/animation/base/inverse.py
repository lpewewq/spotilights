import numpy as np

from ...spotify.models.audio_analysis import Beat
from .sub import SingleSub


class Inverse(SingleSub):
    def __init__(self, config: "Inverse.Config") -> None:
        super().__init__(config)
        self.config: Inverse.Config

    class Config(SingleSub.Config):
        inverse: bool = True

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        colors = super().render(progress, xy)
        if self.config.inverse:
            return colors[::-1]
        else:
            return colors


class InverseOnBeat(Inverse):
    def __init__(self, config: "Inverse.Config") -> None:
        super().__init__(config)

    def on_beat(self, beat: Beat, progress: float) -> None:
        self.config.inverse ^= True
        return super().on_beat(beat, progress)
