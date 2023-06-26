import numpy as np
from scipy import ndimage

from model.Resolutions.AngleResolution import angle_resolution
from model.Resolutions.RangeResolution import range_resolution


def angle_of_arrival_2d(
        tx: int,
        rx: int,
        frame: list,
        freq_slope: float,
        sample_rate: int,
        adc_sample_rate: int,
        data_type: bool
):
    # 1D FFT
    fft_1d = np.fft.fft(frame, axis=2)

    # 2D FFT
    fft_2d = np.fft.fft(fft_1d, axis=0)

    # 3D FFT
    degree_resolution, degrees = angle_resolution(tx=tx, rx=rx)

    fft_3d = np.fft.fft(
        np.pad(
            fft_2d,
            (
                (0, 0),
                (round((180 - len(fft_1d[0])) / 2), round((180 - len(fft_1d[0])) / 2)),
                (0, 0)
            ),
            constant_values=[0, 0]),
        axis=1
    )

    amplitude = 20 * np.log10(np.abs(np.fft.fftshift(fft_3d, axes=1)).sum(0))

    res = ndimage.rotate(amplitude, 90)

    range_resolution_val, distance = range_resolution(
        freq_slope=freq_slope,
        adc_sample_rate=adc_sample_rate,
        sample_rate=sample_rate
    )

    if data_type:
        return [
            res[int(adc_sample_rate / 2):],
            -90,
             90,
            distance.min(),
            int(distance.max() / 2),
            degree_resolution
        ]

    return [
        res,
        -90,
         90,
        distance.min(),
        distance.max(),
        degree_resolution
    ]
