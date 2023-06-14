import numpy as np
from scipy.constants import speed_of_light


def velocity_resolution(
        start_freq: float,
        idle_time: float,
        ramp_time: float,
        chirp_num: float,
        tx: int
):
    c = speed_of_light

    velocity_resolution_val = c / (start_freq * 1_000_000_000 * (idle_time + ramp_time) * chirp_num * tx * 0.000_001)

    velocity = velocity_resolution_val * (np.arange(chirp_num) - (chirp_num / 2))

    return velocity_resolution_val, velocity
