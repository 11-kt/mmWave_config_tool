import numpy as np
import scipy.signal as sig

from model.Resolutions.RangeResolution import range_resolution


def ca_cfar_1d(
        chirp: list,
        guard_cell: int,
        training_cell: int,
        p_fa: float,
        adc_sample_rate: int,
        freq_slope: float,
        sample_rate: int,
        data_type: bool
):

    # 1d FFT
    window_1d = np.abs(np.hamming(adc_sample_rate))
    fft_res = np.abs(np.fft.fft(chirp * window_1d))

    range_resolution_val, distance = range_resolution(
        freq_slope=freq_slope,
        adc_sample_rate=adc_sample_rate,
        sample_rate=sample_rate
    )

    amplitude = 20 * np.log10(np.abs(fft_res))

    # CFAR
    a = training_cell * (p_fa ** (-1 / training_cell) - 1)

    N = guard_cell + training_cell + 1

    p = []
    for i in range(N):
        if i in range(training_cell, N):
            p.append(0)
        else:
            p.append(1)
    p = p / np.sum(p)

    cfar = a * sig.convolve(fft_res, p, mode='same')

    if data_type:
        distance = distance[:int(adc_sample_rate / 2)]
        amplitude = amplitude[:int(adc_sample_rate / 2)]
        cfar = cfar[:int(adc_sample_rate / 2)]

    detected_object = []
    prev_detected = None
    for i in range(len(cfar)):
        if cfar[i] < fft_res[i]:

            if prev_detected is not None:

                if i == prev_detected + 1:

                    if fft_res[i] < fft_res[prev_detected]:
                        prev_detected = i
                        continue

                    else:
                        prev_detected = i
                        del detected_object[-1]
                        detected_object.append([distance[i], amplitude[i], i])
                        continue

            prev_detected = i
            detected_object.append([distance[i], amplitude[i], i])

    return [distance, amplitude, 20 * np.log10(np.abs(cfar)), detected_object]
