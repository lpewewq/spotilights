from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import spotify, strip

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(spotify.router)
api_router.include_router(strip.router)

app.include_router(api_router)
app.mount("/", StaticFiles(directory="svelte/dist", html=True))
