import numpy as np


def ease_linear(x: float) -> float:
    return x


def ease_in_out_sine(x: float) -> float:
    return -(np.cos(np.pi * x) - 1) / 2


def ease_out_quint(x: float) -> float:
    return 1 - (1 - x) ** 5


def ease_out_elastic(x: float) -> float:
    if x == 0.0:
        return 0.0
    elif x == 1.0:
        return 1.0
    else:
        return np.power(2, -10 * x) * np.sin((x * 10 - 0.75) * (2 * np.pi) / 3) + 1


def ease_in_out_back(x: float) -> float:
    c1 = 1.70158
    c2 = c1 * 1.525

    if x < 0.5:
        return (np.power(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
    else:
        return (np.power(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
