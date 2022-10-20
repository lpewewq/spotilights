from ..base import MirrorAnimation, TransitionOnSectionAnimation
from .animation1 import Animation1
from .animation2 import Animation2
from .animation3 import Animation3
from .animation4 import Animation4


class PhilippAnimation(TransitionOnSectionAnimation):
    def __init__(self) -> None:
        animation1 = MirrorAnimation(Animation1(), 2, [False, True])
        animation2 = MirrorAnimation(Animation2(), 2, [False, True])
        animation3 = Animation3()
        animation4 = MirrorAnimation(Animation4(), 2, [False, True])
        animations = [animation1, animation2, animation3, animation4]
        super().__init__(animations=animations, start=0)
