from typing import Optional, Union

from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated

from .composition import Composite
from .inverse import Inverse, InverseOnBeat
from .loudness import ScaleLoudness
from .mirror import Mirror
from .pride import Pride
from .rainbow import Rainbow
from .split import Split
from .strobe import StrobeOnLoudnessGradient
from .theater import Theater
from .transition import TransitionOnSection

Animation = Annotated[
    Union[
        Composite,
        Inverse,
        InverseOnBeat,
        Mirror,
        Pride,
        Rainbow,
        Split,
        StrobeOnLoudnessGradient,
        ScaleLoudness,
        Theater,
        TransitionOnSection,
    ],
    Field(discriminator="name"),
]

StrobeOnLoudnessGradient.update_forward_refs(Animation=Animation)
TransitionOnSection.update_forward_refs(Animation=Animation)
ScaleLoudness.update_forward_refs(Animation=Animation)
InverseOnBeat.update_forward_refs(Animation=Animation)
Composite.update_forward_refs(Animation=Animation)
Inverse.update_forward_refs(Animation=Animation)
Mirror.update_forward_refs(Animation=Animation)
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
