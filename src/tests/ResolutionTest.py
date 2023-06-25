import unittest
from model.Resolutions.RangeResolution import *
from model.Resolutions.VelocityResolution import *
from model.Resolutions.AngleResolution import *


class ResolutionTest(unittest.TestCase):

    def test_bandwidth_1(self):
        self.assertEqual(bandwidth(freq_slope=29.982, adc_sample_rate=128, sample_rate=10_000), 383769600)

    def test_bandwidth_2(self):
        self.assertEqual(bandwidth(freq_slope=29.982, adc_sample_rate=256, sample_rate=10_000), 767539200)

    def test_bandwidth_3(self):
        self.assertEqual(bandwidth(freq_slope=29.982, adc_sample_rate=256, sample_rate=5_000), 1535078400)

    def test_bandwidth_5(self):
        self.assertEqual(bandwidth(freq_slope=0.0, adc_sample_rate=256, sample_rate=5_000), 0)

    def test_bandwidth_6(self):
        self.assertEqual(bandwidth(freq_slope=1.0, adc_sample_rate=0, sample_rate=5_000), 0)

    def test_bandwidth_7(self):
        self.assertEqual(bandwidth(freq_slope=-29.982, adc_sample_rate=128, sample_rate=10_000), -383769600)

    def test_bandwidth_8(self):
        self.assertRaises(ZeroDivisionError, bandwidth, 9, 128, 0)

    def test_range_res_1(self):
        self.assertEqual(int(range_res(383769600) * 1e16), 3905891164907277)

    def test_range_res_2(self):
        self.assertEqual(int(range_res(767539200) * 1e16), 1952945582453638)

    def test_range_res_3(self):
        self.assertEqual(int(range_res(-383769600) * 1e16), -3905891164907277)

    def test_range_res_4(self):
        self.assertRaises(ZeroDivisionError, range_res, 0)

    def test_range_resolution_1(self):
        adc_sample_rate = 512
        res, dis = range_resolution(freq_slope=15.182, adc_sample_rate=adc_sample_rate, sample_rate=10_000)

        self.assertEqual(int(res * 1e16), 1928376184070774)

        self.assertEqual(int(dis[-1]), int(res * adc_sample_rate))

    def test_range_resolution_2(self):
        adc_sample_rate = 1024
        res, dis = range_resolution(freq_slope=34.076, adc_sample_rate=adc_sample_rate, sample_rate=4_750)

        self.assertEqual(int(res * 1e16), 204049601370718)

        self.assertEqual(int(dis[-1]), int(res * adc_sample_rate))

    def test_range_resolution_3(self):
        adc_sample_rate = 0
        self.assertRaises(ZeroDivisionError, range_resolution, 34.076, adc_sample_rate, 4_750)

    def test_range_resolution_4(self):
        adc_sample_rate = 32
        self.assertRaises(ZeroDivisionError, range_resolution, 34.076, adc_sample_rate, 0)

    def test_range_resolution_5(self):
        adc_sample_rate = 1024
        res, dis = range_resolution(freq_slope=-34.076, adc_sample_rate=adc_sample_rate, sample_rate=4_750)

        self.assertEqual(int(res * 1e16), -204049601370718)

        self.assertEqual(int(dis[-1]), int(res * adc_sample_rate))

    def test_velocity_resolution_1(self):
        res, vel = velocity_resolution(start_freq=77.0, idle_time=100, ramp_time=60, chirp_num=128, tx=2)

        self.assertEqual(int(res * 1e17), 9505391956676136)

        self.assertEqual(int(vel[-1] * 1e15), 5988396932705966)

    def test_velocity_resolution_2(self):
        res, vel = velocity_resolution(start_freq=79.0, idle_time=10, ramp_time=6, chirp_num=1024, tx=1)

        self.assertEqual(int(res * 1e17), 23161872805824764)

        self.assertEqual(int(vel[-1] * 1e15), 118357170037764528)

    def test_velocity_resolution_3(self):
        res, vel = velocity_resolution(start_freq=76.0, idle_time=0, ramp_time=6, chirp_num=512, tx=2)

        self.assertEqual(int(res * 1e17), 64203086023163384)

        self.assertEqual(int(vel[-1] * 1e15), 163717869359066624)

    def test_velocity_resolution_4(self):
        res, vel = velocity_resolution(start_freq=76.0, idle_time=110, ramp_time=0, chirp_num=512, tx=2)

        self.assertEqual(int(res * 1e17), 3501986510354365)

        self.assertEqual(int(vel[-1] * 1e15), 8930065601403632)

    def test_velocity_resolution_5(self):
        self.assertRaises(ZeroDivisionError, velocity_resolution, 0.0, 110, 10, 512, 2)

    def test_velocity_resolution_6(self):
        self.assertRaises(ZeroDivisionError, velocity_resolution, 76.0, 110, 10, 0, 2)

    def test_velocity_resolution_7(self):
        self.assertRaises(ZeroDivisionError, velocity_resolution, 76.0, 110, 10, 32, 0)

    def test_angle_resolution_1(self):
        res, deg = angle_resolution(tx=2, rx=4)

        self.assertEqual(int(res * 1e14), 1432394487827058)

        self.assertEqual(int(deg * 1e14), 1256637061435917)

    def test_angle_resolution_2(self):
        res, deg = angle_resolution(tx=1, rx=1)

        self.assertEqual(int(res * 1e14), 11459155902616464)

        self.assertEqual(int(deg * 1e14), 157079632679489)

    def test_angle_resolution_3(self):
        self.assertRaises(ZeroDivisionError, angle_resolution, 0, 1)

    def test_angle_resolution_4(self):
        self.assertRaises(ZeroDivisionError, angle_resolution, 1, 0)

    def test_angle_resolution_5(self):
        res, deg = angle_resolution(tx=2, rx=1)

        self.assertEqual(int(res * 1e14), 5729577951308232)

        self.assertEqual(int(deg * 1e14), 314159265358979)

    def test_angle_resolution_6(self):
        res, deg = angle_resolution(tx=2, rx=2)

        self.assertEqual(int(res * 1e14), 2864788975654116)

        self.assertEqual(int(deg * 1e14), 628318530717958)

    def test_angle_resolution_7(self):
        res, deg = angle_resolution(tx=2, rx=3)

        self.assertEqual(int(res * 1e14), 1909859317102743)

        self.assertEqual(int(deg * 1e14), 942477796076938)
