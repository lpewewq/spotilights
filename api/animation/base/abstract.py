from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, Type

import numpy as np
from pydantic import BaseModel, validator

from ...spotify.models import AudioAnalysis, Bar, Beat, Section, Segment, Tatum

animation_subclass_registry = dict()


class Animation(ABC):
    """Interface for animations."""

    def __init__(self, config: "Animation.Config") -> None:
        super().__init__()
        self.config = config

    def __init_subclass__(cls) -> None:
        if ABC not in cls.__bases__:
            animation_subclass_registry[cls.__name__] = cls
        return super().__init_subclass__()

    class Config(BaseModel):
        def concrete_schema(self, *args, **kwargs):
            return self.schema(*args, **kwargs).get("properties", {})

        @property
        def needs_spotify(self) -> bool:
            """Identify spotify dependant animations"""
            return False

    def update_config(self, config: "Animation.Config") -> bool:
        if self.config == config:
            return False
        self._change_trigger = True
        self.config = config
        return True

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.config})"

    def on_track_change(self, analysis: AudioAnalysis) -> None:
        """Track change callback"""
        pass

    def on_section(self, section: Section, progress: float) -> None:
        """Section callback"""
        pass

    def on_bar(self, bar: Bar, progress: float) -> None:
        """Bar callback"""
        pass

    def on_beat(self, beat: Beat, progress: float) -> None:
        """Beat callback"""
        pass

    def on_tatum(self, tatum: Tatum, progress: float) -> None:
        """Tatum callback"""
        pass

    def on_segment(self, segment: Segment, progress: float) -> None:
        """Segment callback"""
        pass

    def change_callback(self, xy: np.ndarray) -> None:
        """Callback function used by @change_callback decorator when the xy coordinates change"""
        pass

    @abstractmethod
    def render(self, progress: float, xy: np.ndarray) -> np.ndarray:
        """Return rendered animation. For each xy coordinate return a Color"""


class AnimationModel(BaseModel):
    animation: Type[Animation]
    config: Optional[Animation.Config]

    class Config:
        json_encoders = {ABCMeta: lambda c: c.__name__}

    @validator("animation", pre=True)
    def validate_animation(cls, v):
        try:
            if isinstance(v, str):
                animation_cls = animation_subclass_registry[v]
            else:
                animation_cls = v
            return animation_cls
        except KeyError:
            raise ValueError(f'Unknown animation "{v}".')

    @validator("config", pre=True, always=True)
    def validate_config(cls, v, values):
        if "animation" not in values:
            raise ValueError("Animation class not found for config.")
        animation_cls: Animation = values["animation"]
        if v is None:
            return animation_cls.Config()
        else:
            return animation_cls.Config.parse_obj(v)

    def construct(self):
        return self.animation(self.config)

    def concrete_schema(self, *args, **kwargs):
        return {"animation": self.animation.__name__, "config": self.config.concrete_schema(*args, **kwargs)}
