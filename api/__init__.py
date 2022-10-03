from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from .animation import router as animation_router
from .spotify.routes import router as spotify_router
from .strip.routes import router as strip_router

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(spotify_router)
api_router.include_router(strip_router)
api_router.include_router(animation_router)

app.include_router(api_router)
app.mount("/", StaticFiles(directory="svelte/dist", html=True))
