import unittest

from model.PostProc.FFT_2D import fft_2d
from model.PostProc.FFT_3D import angle_of_arrival_2d
from model.Resolutions.VelocityResolution import velocity_resolution
from src.model.PostProc.FFT_1D import *


class ResolutionTest(unittest.TestCase):

    # Объект на расстоянии 1.7 м
    def test_range_fft_1(self):
        with open("tests_data/chirp_1.txt", "r") as f:
            chirp = [np.int16(line.strip()) for line in f]

        res = fft_1d(
            chirp=chirp,
            freq_slope=29.982,
            adc_sample_rate=256,
            sample_rate=10_000,
            type_plot=2,
            data_type=True
        )

        m = 0.0
        pos = 0
        for i in range(len(res[1])):
            if m < res[1][i] - 1e-10:
                m = res[1][i]
                pos = res[0][i]

        self.assertEqual(int(pos * 1e7), 17576510)

    # Объект на расстоянии 3.4 м
    def test_range_fft_2(self):
        with open("tests_data/chirp_2.txt", "r") as f:
            chirp = [complex(line.strip()) for line in f]

        res = fft_1d(
            chirp=chirp,
            freq_slope=29.982,
            adc_sample_rate=128,
            sample_rate=15_000,
            type_plot=2,
            data_type=False
        )

        m = 0.0
        pos = 0
        for i in range(len(res[1])):
            if m < res[1][i] - 1e-10:
                m = res[1][i]
                pos = res[0][i]

        self.assertEqual(int(pos * 1e7), 35153020)

    def test_range_fft_real_1(self):
        with open("tests_data/chirp_2.txt", "r") as f:
            chirp = [complex(line.strip()) for line in f]

        res = fft_1d(
            chirp=chirp,
            freq_slope=29.982,
            adc_sample_rate=128,
            sample_rate=15_000,
            type_plot=0,
            data_type=False
        )

        for i in range(1, int(len(res[1]) / 2)):
            self.assertEqual(int(res[1][i] * 1e10), int(res[1][len(res[1]) - i] * 1e10))

    def test_range_fft_image_1(self):
        with open("tests_data/chirp_2.txt", "r") as f:
            chirp = [complex(line.strip()) for line in f]

        res = fft_1d(
            chirp=chirp,
            freq_slope=29.982,
            adc_sample_rate=128,
            sample_rate=15_000,
            type_plot=1,
            data_type=False
        )

        for i in range(1, int(len(res[1]) / 2)):
            self.assertEqual(int(res[1][i] * 1e10), int(res[1][len(res[1]) - i] * 1e10))

    # Объект на расстоянии ~5.1м, скорость ~1.8м, направление в сторону устройства
    def test_velocity_fft_1(self):
        with open("tests_data/frame_1.txt", "r") as f:
            data = [complex(line.strip()) for line in f]

        adc_sample_rate = 256
        num_chirps = 128
        frame = []
        current_ind = 0
        for i in range(num_chirps):
            frame.append(data[current_ind:current_ind + adc_sample_rate])
            current_ind += adc_sample_rate

        res = fft_2d(
            tx=2,
            frame=frame,
            data_type=False,
            idle_time=100,
            ramp_time=60,
            chirp_num=num_chirps,
            freq_slope=29.982,
            start_freq=77.0,
            sample_rate=4_750,
            adc_sample_rate=adc_sample_rate,
            is_3d=False
        )

        m = 0.0
        velocity = 0
        range_to_obj = 0
        for i in range(len(res[0])):
            for j in range(len(res[0][i])):
                if res[0][i][j] - 1e-10 > m:
                    m = res[0][i][j]
                    range_to_obj = i
                    velocity = j

        vel_res, _ = velocity_resolution(start_freq=77.0, idle_time=100, ramp_time=60, chirp_num=128, tx=2)
        self.assertEqual(int((res[1] + velocity * vel_res) * 1e10), -18060244717)

        range_res, _ = range_resolution(freq_slope=29.982, adc_sample_rate=adc_sample_rate, sample_rate=4_750)
        self.assertEqual(int(((len(res[0]) - range_to_obj - 1) * range_res) * 1e10), 51020703341)

    # Объект на расстоянии ~2м, под углом 22 градуса
    def test_angle_fft_1(self):
        with open("tests_data/frame_2.txt", "r") as f:
            data = [complex(line.strip()) for line in f]

        adc_sample_rate = 256
        num_chirps = 128
        frame = []
        current_ind = 0
        for i in range(num_chirps):
            antenna0 = data[(0 * 32768) + current_ind:(0 * 32768) + current_ind + adc_sample_rate]
            antenna1 = data[(1 * 32768) + current_ind:(1 * 32768) + current_ind + adc_sample_rate]
            antenna2 = data[(2 * 32768) + current_ind:(2 * 32768) + current_ind + adc_sample_rate]
            antenna3 = data[(3 * 32768) + current_ind:(3 * 32768) + current_ind + adc_sample_rate]
            frame.append([antenna0, antenna1, antenna2, antenna3])
            current_ind += adc_sample_rate

        res = angle_of_arrival_2d(
            tx=1,
            rx=3,
            frame=frame,
            freq_slope=29.982,
            sample_rate=4_750,
            adc_sample_rate=adc_sample_rate,
            data_type=False
        )

        m = 0.0
        angle = 0
        range_to_obj = 0
        for i in range(len(res[0])):
            for j in range(len(res[0][i])):
                if res[0][i][j] - 1e-10 > m:
                    m = res[0][i][j]
                    range_to_obj = i
                    angle = j

        if abs(angle) > 90:
            angle = abs(angle) - 90
        self.assertEqual(angle, 22)

        range_res, _ = range_resolution(freq_slope=29.982, adc_sample_rate=adc_sample_rate, sample_rate=4_750)
        self.assertEqual(int(((len(res[0]) - range_to_obj - 1) * range_res) * 1e10), 20408281336)
