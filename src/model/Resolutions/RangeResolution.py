import numpy as np
from scipy.constants import speed_of_light


def range_resolution(
    freq_slope: float,
    adc_sample_rate: int,
    sample_rate: int
):

    bandwidth_chirp = bandwidth(freq_slope, adc_sample_rate, sample_rate)

    range_resolution_val = range_res(bandwidth_chirp)

    distance = np.arange(adc_sample_rate) * range_resolution_val

    return range_resolution_val, distance


def range_res(bandwidth_chirp: float):
    c = speed_of_light

    return c / (2 * bandwidth_chirp)


def bandwidth(
        freq_slope: float,
        adc_sample_rate: int,
        sample_rate: int
):
    return freq_slope * 1_000_000 * adc_sample_rate / sample_rate * 1_000
