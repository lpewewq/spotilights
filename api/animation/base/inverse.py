from .absract import Animation
from .sub import SubAnimation


class InverseAnimation(SubAnimation):
    def __init__(self, animation: Animation) -> None:
        super().__init__(animations=[animation], inverse=[True])
