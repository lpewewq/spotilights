import numpy as np
from pydantic import Field

from ...color import Color
from .bpm import BPM


class Fill(BPM):
    def __init__(self, config: "Fill.Config") -> None:
        super().__init__(config)
        self.config: Fill.Config

    class Config(BPM.Config):
        color: Color = Field(Color(r=255), config_type="Color", title="Fill Color")

    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        color = self.config.color * self.beat(self.bpm)
        return np.full(len(xy), color)
