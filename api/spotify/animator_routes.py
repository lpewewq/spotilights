from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, FilePath, validator

from ..animation.base import AnimationModel
from . import spotify_animator


class AnimationModelPayload(BaseModel):
    file: FilePath
    model: Optional[AnimationModel]

    @validator("file", pre=True)
    def file_validator(cls, v):
        return Path("animation_data").joinpath(Path(v))


router = APIRouter(prefix="/animator")


@router.on_event("shutdown")
def shutdown():
    spotify_animator.stop()


@router.post("/stop")
async def stop_animator():
    spotify_animator.stop()


@router.post("/start")
async def start_rainbow(payload: AnimationModelPayload):
    if payload.model:
        spotify_animator.start(payload.model.construct())
        with open(payload.file, "w") as file:
            file.write(payload.model.json(indent=2))
    else:
        model = AnimationModel.parse_file(payload.file)
        spotify_animator.start(model.construct())
