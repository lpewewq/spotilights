from ..base import Mirror, ScaleLoudness, SingleSub, StrobeOnLoudnessGradient, TransitionOnSection
from ..basic import Animation1, Animation2, Animation3, Animation4


class PhilippsAnimation(SingleSub):
    def __init__(self) -> None:
        animation1 = Mirror(Animation1(), 2, [False, True])
        animation2 = Mirror(Animation2(), 2, [False, True])
        animation3 = Animation3()
        animation4 = Mirror(Animation4(), 2, [False, True])
        animations = [animation1, animation2, animation3, animation4]
        super().__init__(StrobeOnLoudnessGradient(ScaleLoudness(TransitionOnSection(animations))))
