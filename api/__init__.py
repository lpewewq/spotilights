from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from .spotify.animator_routes import router as animator_router
from .spotify.client_routes import router as client_router
from .strip.routes import router as strip_router

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(animator_router)
api_router.include_router(client_router)
api_router.include_router(strip_router)

app.include_router(api_router)
app.mount("/", StaticFiles(directory="svelte/dist", html=True))
