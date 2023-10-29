from typing import Optional, Union

from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated

from .animation1 import Animation1
from .animation2 import Animation2
from .animation3 import Animation3
from .animation4 import Animation4
from .bell import Bell
from .composition import Composite
from .fill import Fill
from .inverse import Inverse, InverseOnEvent
from .loudness import ScaleLoudness
from .mirror import Mirror
from .pride import Pride
from .rainbow import Rainbow
from .scale import BeatScale
from .shift import Shift
from .split import Split
from .strobe import StrobeOnLoudnessGradient
from .test2d import Test2D
from .theater import Theater
from .transition import TransitionOnSection
from .wave2d import Wave2D

Animation = Annotated[
    Union[
        Animation1,
        Animation2,
        Animation3,
        Animation4,
        Composite,
        Fill,
        Inverse,
        InverseOnEvent,
        Mirror,
        Pride,
        Rainbow,
        BeatScale,
        Bell,
        Shift,
        Split,
        StrobeOnLoudnessGradient,
        ScaleLoudness,
        Theater,
        TransitionOnSection,
        Wave2D,
        Test2D,
    ],
    Field(discriminator="name"),
]

StrobeOnLoudnessGradient.update_forward_refs(Animation=Animation)
TransitionOnSection.update_forward_refs(Animation=Animation)
InverseOnEvent.update_forward_refs(Animation=Animation)
ScaleLoudness.update_forward_refs(Animation=Animation)
BeatScale.update_forward_refs(Animation=Animation)
Composite.update_forward_refs(Animation=Animation)
Inverse.update_forward_refs(Animation=Animation)
Mirror.update_forward_refs(Animation=Animation)
Shift.update_forward_refs(Animation=Animation)
Split.update_forward_refs(Animation=Animation)


class AnimationModel(BaseModel):
    name: str
    animation: Animation
    needs_spotify: Optional[bool] = None

    @validator("needs_spotify", always=True)
    def needs_spotify_validator(cls, v, values):
        animation = values.get("animation")
        if animation is None:
            return v
        return animation.needs_spotify
