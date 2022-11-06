from abc import ABCMeta
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ValidationError, validator

from ...animation.base import AnimationModel
from ...config import settings
from . import spotify_animator


router = APIRouter(prefix="/animator")


@router.on_event("shutdown")
def shutdown():
    spotify_animator.stop()


@router.post("/stop")
def stop_animator():
    spotify_animator.stop()


class AnimationModelPayload(BaseModel):
    name: str
    model: AnimationModel
    needs_spotify: bool = None
    concrete_schema: Any = None

    class Config:
        json_encoders = {ABCMeta: lambda c: c.__name__}

    @validator("needs_spotify", always=True)
    def needs_spotify_validator(cls, v, values):
        return values.get("model").config.needs_spotify

    @validator("concrete_schema", always=True)
    def concrete_schema_validator(cls, v, values):
        return values.get("model").concrete_schema()

    @property
    def file(self):
        return settings.animation_data_path.joinpath(Path(f"{self.name}.json"))


@router.post("/start")
async def start_animation(payload: AnimationModelPayload):
    spotify_animator.start(payload.model)
    try:
        with open(payload.file, "w") as file:
            file.write(payload.json(indent=2, exclude={"needs_spotify", "concrete_schema"}))
    except TypeError as e:
        print("start_animation", payload.file, e)


@router.get("/models")
def get_models():
    models = []
    for path in settings.animation_data_path.glob("*.json"):
        try:
            payload = AnimationModelPayload.parse_file(path)
            models.append(payload)
        except (ValidationError, JSONDecodeError, AttributeError) as e:
            print("get_models", path, e)
    return models
