from json import JSONDecodeError

from fastapi import APIRouter
from pydantic import ValidationError

from ...animation import AnimationModel
from ...config import settings
from . import spotify_animator

router = APIRouter(prefix="/animator")


@router.on_event("shutdown")
def shutdown():
    spotify_animator.stop()


@router.post("/stop")
def stop_animator():
    spotify_animator.stop()


@router.post("/start")
async def start_animation(animation_model: AnimationModel):
    spotify_animator.start(animation_model)


@router.get("/schema")
def get_schema():
    return AnimationModel.schema()


@router.get("/models")
def get_models():
    models = []
    for path in settings.animation_data_path.glob("*.json"):
        try:
            payload = AnimationModel.parse_file(path)
            models.append(payload)
        except (ValidationError, JSONDecodeError, AttributeError) as e:
            print("get_models", path, e)
    return models
