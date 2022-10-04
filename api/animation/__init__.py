from fastapi import APIRouter

router = APIRouter(prefix="/animation")

from .philipp import *
from .fill import *
from .pride import *
from .rainbow import *
from .theater import *
