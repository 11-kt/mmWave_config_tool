import numpy as np
from model.Resolutions.RangeResolution import range_resolution


# Range FFT
def fft_1d(
        chirp: list,
        type_plot: int,
        data_type: bool,
        freq_slope: float,
        sample_rate: int,
        adc_sample_rate: int
):
    # Окно
    window_1d = np.abs(np.hamming(adc_sample_rate))

    # 3 Режима, БПФ по вещественной части, по мнимой и по комплексным
    if type_plot == 0:
        for j in range(len(chirp)):
            chirp[j] = chirp[j].real
    elif type_plot == 1:
        for j in range(len(chirp)):
            chirp[j] = chirp[j].imag

    # 1d FFT
    fft_res = np.fft.fft(chirp * window_1d)

    range_resolution_val, distance = range_resolution(
        freq_slope=freq_slope,
        adc_sample_rate=adc_sample_rate,
        sample_rate=sample_rate
    )

    amplitude = 20 * np.log10(np.abs(fft_res))

    if data_type:
        return [distance[:int(adc_sample_rate / 2)], amplitude[:int(adc_sample_rate / 2)]]

    return [distance, amplitude]
