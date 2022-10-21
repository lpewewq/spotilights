from ..base import Mirror, TransitionOnSection
from ..basic import Animation1, Animation2, Animation3, Animation4


class PhilippsAnimation(TransitionOnSection):
    def __init__(self) -> None:
        animation1 = Mirror(Animation1(), 2, [False, True])
        animation2 = Mirror(Animation2(), 2, [False, True])
        animation3 = Animation3()
        animation4 = Mirror(Animation4(), 2, [False, True])
        animations = [animation1, animation2, animation3, animation4]
        super().__init__(animations=animations, start=0)
