from abc import ABCMeta
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, ValidationError

from ..animation.base import AnimationModel
from ..config import settings
from . import spotify_animator


class AnimationModelPayload(BaseModel):
    name: str
    model: AnimationModel

    class Config:
        json_encoders = {ABCMeta: lambda c: c.__name__}

    @property
    def file(self):
        return settings.animation_data_path.joinpath(Path(f"{self.name}.json"))


router = APIRouter(prefix="/animator")


@router.on_event("shutdown")
def shutdown():
    spotify_animator.stop()


@router.post("/stop")
async def stop_animator():
    spotify_animator.stop()


@router.post("/start")
async def start_animation(payload: AnimationModelPayload):
    spotify_animator.start(payload.model)
    with open(payload.file, "w") as file:
        file.write(payload.json(indent=2))


@router.get("/models")
async def get_models():
    models = []
    for path in settings.animation_data_path.glob("*.json"):
        try:
            models.append(AnimationModelPayload.parse_file(path))
        except ValidationError as e:
            print(path, e)
    return models
