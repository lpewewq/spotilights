from abc import ABCMeta
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel, ValidationError

from ..animation.base import AnimationModel
from ..config import settings
from . import spotify_animator


class AnimationModelPayload(BaseModel):
    name: str
    model: AnimationModel
    model_schema: Optional[Any]
    needs_spotify: Optional[bool]

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
def stop_animator():
    spotify_animator.stop()


@router.post("/start")
async def start_animation(payload: AnimationModelPayload):
    spotify_animator.start(payload.model)
    try:
        with open(payload.file, "w") as file:
            file.write(payload.json(indent=2, exclude={"needs_spotify", "model_schema"}))
    except TypeError as e:
        print("start_animation", payload.file, e)


@router.get("/models")
def get_models():
    models = []
    for path in settings.animation_data_path.glob("*.json"):
        try:
            payload = AnimationModelPayload.parse_file(path)
            payload.model_schema = payload.model.config.schema()
            payload.needs_spotify = payload.model.config.needs_spotify
            models.append(payload)
        except (ValidationError, JSONDecodeError) as e:
            print("get_models", path, e)
    return models
