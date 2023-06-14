import numpy as np
import scipy.ndimage as ndimage

from model.Resolutions.RangeResolution import range_resolution
from model.Resolutions.VelocityResolution import velocity_resolution


# Doppler FFT
def fft_2d(
        tx: int,
        frame: list,
        data_type: bool,
        idle_time: float,
        ramp_time: float,
        chirp_num: int,
        freq_slope: float,
        start_freq: float,
        sample_rate: int,
        adc_sample_rate: int,
        is_3d: bool
):

    window_1d = np.hamming(adc_sample_rate)
    window_2d = np.sqrt(np.outer(chirp_num, window_1d))

    # 1d FFT
    fft_1dim = np.fft.fft(frame * window_2d, axis=1)

    # 2d FFT
    fft_2dim = np.fft.fft(fft_1dim, axis=0)

    range_resolution_val, distance = range_resolution(
        freq_slope=freq_slope,
        adc_sample_rate=adc_sample_rate,
        sample_rate=sample_rate
    )

    velocity_resolution_val, velocity = velocity_resolution(
        start_freq=start_freq,
        idle_time=idle_time,
        ramp_time=ramp_time,
        chirp_num=chirp_num,
        tx=tx
    )

    amplitude = 20 * np.log10(np.abs((np.fft.fftshift(fft_2dim, axes=0))))

    res = ndimage.rotate(amplitude, 90)

    if is_3d:
        if data_type:
            x, y = np.meshgrid(distance[:int(adc_sample_rate / 2)], velocity)

            return [np.flip(x, 1), y, amplitude[:, int(adc_sample_rate / 2):]]

        else:
            x, y = np.meshgrid(distance, velocity)

            return [x, y, amplitude]

    if data_type:
        return [
            res[int(adc_sample_rate / 2):],
            velocity.min(),
            velocity.max(),
            distance.min(),
            int(distance.max() / 2)]

    return [
        res,
        velocity.min(),
        velocity.max(),
        distance.min(),
        distance.max()
    ]
