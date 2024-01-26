import time

import numpy as np


def beat(bpm: float, shift: float = 0.0, low=0.0) -> float:
    bps2pi = 2 * np.pi * bpm / 60
    beat = (np.sin(-time.time() * bps2pi + shift) + 1) / 2
    return low + (1 - low) * beat

def bell(x):
    return 1 / (1 + x**2) ** 1.5
