import unittest
import numpy as np

from model.PostProc.CA_CFAR_1D import ca_cfar_1d
from model.PostProc.ObjectDetection import detected_object


class ObjDetectionTest(unittest.TestCase):

    # Объект на расстоянии 1.7 м
    def test_ca_cfar_1(self):
        with open("tests_data/chirp_1.txt", "r") as f:
            chirp = [np.int16(line.strip()) for line in f]

        res = ca_cfar_1d(
            chirp=chirp,
            guard_cell=1,
            training_cell=20,
            p_fa=1e-1,
            adc_sample_rate=256,
            freq_slope=29.982,
            sample_rate=10_000,
            data_type=True
        )

        self.assertEqual(len(res[3]), 1)
        self.assertEqual(int(res[3][0][0] * 1e7), 17576510)

    # Объект на расстоянии 1.7 м
    def test_ca_cfar_2(self):
        with open("tests_data/chirp_2.txt", "r") as f:
            chirp = [complex(line.strip()) for line in f]

        res = ca_cfar_1d(
            chirp=chirp,
            guard_cell=2,
            training_cell=16,
            p_fa=1e-1,
            adc_sample_rate=128,
            freq_slope=29.982,
            sample_rate=15_000,
            data_type=False
        )

        self.assertEqual(len(res[3]), 2)
        self.assertEqual(int(res[3][0][0] * 1e7), 35153020)

    # Объект на расстоянии ~2м, под углом 22 градуса
    def test_detected_obj_1(self):
        with open("tests_data/frame_2.txt", "r") as f:
            data = [complex(line.strip()) for line in f]

        adc_sample_rate = 256
        chirp = []
        for i in range(adc_sample_rate):
            chirp.append(data[i])

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

        res = detected_object(
            chirp=chirp,
            frame=frame,
            guard_cell=1,
            training_cell=20,
            p_fa=1e-2,
            data_type=False,
            tx=1,
            rx=3,
            freq_slope=29.982,
            sample_rate=4_750,
            adc_sample_rate=adc_sample_rate
        )

        self.assertEqual(int(res[0][0][0] * 1e10), 20408281336)
