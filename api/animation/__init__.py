from typing import Optional, Union

from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated

from .mirror import Mirror
from .pride import Pride
from .rainbow import Rainbow
from .split import Split
from .theater import Theater

Animation = Annotated[Union[Mirror, Split, Rainbow, Pride, Theater], Field(discriminator="name")]

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
