from fastapi import APIRouter

router = APIRouter(prefix="/animation")

from .fill import *
from .pride import *
from .rainbow import *
from .theater import *
