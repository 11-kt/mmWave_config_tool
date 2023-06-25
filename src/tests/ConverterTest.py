import unittest
from model.ConvertingValues import ConvertingValues


class ConverterTest(unittest.TestCase):

    # 100 ms -> 100_000_000 ns
    def test_convert_ms_ns_1(self):
        cv = ConvertingValues()

        value = 100
        convert_value = cv.convert_ms_ns(value)

        self.assertEqual(convert_value, 100_000_000)
        self.assertNotEqual(convert_value, 1_000_000)

    # 0 ms -> 0 ns
    def test_convert_ms_ns_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.convert_ms_ns(value)

        self.assertEqual(convert_value, 0)
        self.assertNotEqual(convert_value, 1_000_000)

    # 10 mcs -> 100_000 ns
    def test_convert_mcs_ns_1(self):
        cv = ConvertingValues()

        value = 10
        convert_value = cv.convert_mcs_ns(value)

        self.assertEqual(convert_value, 10_000)
        self.assertNotEqual(convert_value, 1_000_000)

    # 0 ms -> 0 ns
    def test_convert_mcs_ns_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.convert_mcs_ns(value)

        self.assertEqual(convert_value, 0)
        self.assertNotEqual(convert_value, 1)

    # 10 GHz -> 10_000_000_000 Hz
    def test_convert_ghz_hz_1(self):
        cv = ConvertingValues()

        value = 10
        convert_value = cv.convert_ghz_hz(value)

        self.assertEqual(convert_value, 10_000_000_000)

    # 0 GHz -> 0 Hz
    def test_convert_ghz_hz_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.convert_ghz_hz(value)

        self.assertEqual(convert_value, 0)

    # 10 MHz -> 10_000 kHz
    def test_convert_mhz_khz_1(self):
        cv = ConvertingValues()

        value = 10
        convert_value = cv.convert_mhz_khz(value)

        self.assertEqual(convert_value, 10_000)

    # 0 MHz -> 0 kHz
    def test_convert_mhz_khz_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.convert_mhz_khz(value)

        self.assertEqual(convert_value, 0)

    # 10 MHz -> 10_000_000 Hz
    def test_convert_mhz_hz_1(self):
        cv = ConvertingValues()

        value = 10
        convert_value = cv.convert_mhz_hz(value)

        self.assertEqual(convert_value, 10_000_000)

    # 0 MHz -> 0 Hz
    def test_convert_mhz_hz_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.convert_mhz_hz(value)

        self.assertEqual(convert_value, 0)

    # Перевод частоты в деления
    # 1 деление = 53.644 Hz
    # Freq = 80.5 GHz
    # 80.5 Ghz -> 80_500_000_000 Hz / 53.644 Hz ~ 1_500_633_808
    def test_start_freq_translation_1(self):
        cv = ConvertingValues()

        value = 80.5
        convert_value = cv.start_freq_translation(value)

        self.assertEqual(convert_value, 1_500_633_808)
        self.assertNotEqual(convert_value, 1_500_633_809)

    # Freq = 0 Ghz
    def test_start_freq_translation_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.start_freq_translation(value)

        self.assertEqual(convert_value, 0)
        # Freq = 0 Ghz

    # Перевод частоты уклона в деления
    # 1 деление = 48.279 kHz/uS
    # Freq_slope = 99.0 MHz/uS
    # 99.0 MHz/uS -> 99_000 Hz / 48.279 Hz ~ 2_051
    def test_freq_slope_translation_1(self):
        cv = ConvertingValues()

        value = 99.0
        convert_value = cv.freq_slope_translation(value)

        self.assertEqual(convert_value, 2_051)
        self.assertNotEqual(convert_value, 2_052)

    # Freq_slope = 0.0 MHz/uS
    def test_freq_slope_translation_2(self):
        cv = ConvertingValues()

        value = 0.0
        convert_value = cv.freq_slope_translation(value)

        self.assertEqual(convert_value, 0)

    # Freq_slope = -100.0 MHz/uS
    # 100.0 MHz/uS -> -100_000 Hz / 48.279 Hz ~ -2_071
    def test_freq_slope_translation_3(self):
        cv = ConvertingValues()

        value = -100.0
        convert_value = cv.freq_slope_translation(value)

        self.assertEqual(convert_value, -2_071)
        self.assertNotEqual(convert_value, -2_072)

    # Перевод значения idle_time из мкс в деления
    def test_idle_time_converter_1(self):
        cv = ConvertingValues()

        value = 5_242.87
        convert_value = cv.idle_time_converter(value)

        self.assertEqual(convert_value, 524_287)

    # Перевод значения idle_time из мкс в деления
    def test_idle_time_converter_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.idle_time_converter(value)

        self.assertEqual(convert_value, 0)

    # Перевод значения idle_time из мкс в деления
    def test_adc_start_time_converter_1(self):
        cv = ConvertingValues()

        value = 40.95
        convert_value = cv.adc_start_time_converter(value)

        self.assertEqual(convert_value, 4095)

    # Перевод значения idle_time из мкс в деления
    def test_adc_start_time_converter_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.adc_start_time_converter(value)

        self.assertEqual(convert_value, 0)

    # Перевод значения idle_time из мкс в деления
    def test_ramp_end_time_converter_1(self):
        cv = ConvertingValues()

        value = 5000.00
        convert_value = cv.ramp_end_time_converter(value)

        self.assertEqual(convert_value, 500_000)

    # Перевод значения idle_time из мкс в деления
    def test_ramp_end_time_converter_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.ramp_end_time_converter(value)

        self.assertEqual(convert_value, 0)

    # Объединение значений tx0-tx2 out power backoff code
    # b7:0 TX0 output power back off
    # b15:8 TX1 output power back off
    # b23:16 TX2 output power back off
    # b31:24 Reserved
    # tx0 = 9, tx1 = 6, tx2 = 4 -> 0000_0000_0000_0100_0000_0110_0000_1001b = 263689d
    def test_tx_out_power_backoff_code_concatenate_1(self):
        cv = ConvertingValues()

        tx0 = 9
        tx1 = 6
        tx2 = 4
        convert_value = cv.tx_out_power_backoff_code_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 263689)

    # tx0 = 0, tx1 = 6, tx2 = 4 -> 0000_0000_0000_0100_0000_0110_0000_0000b = 263680d
    def test_tx_out_power_backoff_code_concatenate_2(self):
        cv = ConvertingValues()

        tx0 = 0
        tx1 = 6
        tx2 = 4
        convert_value = cv.tx_out_power_backoff_code_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 263680)

    # tx0 = 7, tx1 = 0, tx2 = 4 -> 0000_0000_0000_0100_0000_0000_0000_0111b = 262151d
    def test_tx_out_power_backoff_code_concatenate_3(self):
        cv = ConvertingValues()

        tx0 = 7
        tx1 = 0
        tx2 = 4
        convert_value = cv.tx_out_power_backoff_code_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 262151)

    # tx0 = 7, tx1 = 5, tx2 = 0 -> 0000_0000_0000_0000_0000_0101_0000_0111b = 1287d
    def test_tx_out_power_backoff_code_concatenate_4(self):
        cv = ConvertingValues()

        tx0 = 7
        tx1 = 5
        tx2 = 0
        convert_value = cv.tx_out_power_backoff_code_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 1287)

    # tx0 = 0, tx1 = 0, tx2 = 0 -> 0000_0000_0000_0000_0000_0000_0000_0000b = 0d
    def test_tx_out_power_backoff_code_concatenate_5(self):
        cv = ConvertingValues()

        tx0 = 0
        tx1 = 0
        tx2 = 0
        convert_value = cv.tx_out_power_backoff_code_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 0)

    # Объединение значений tx0-tx2 phase shift
    # 1 LSB = 360/2^6 = 5.625 degrees
    # b1:0 Reserved (set to 0b00)
    # b7:2 TX0 phase shift value
    # b9:8 Reserved (set to 0b00)
    # b15:10 TX1 phase shift value
    # b17:16 Reserved (set to 0b00)
    # b23:18 TX2 phase shift value
    # b31:24 Reserved
    # tx0 = 358, tx1 = 350, tx2 = 340 -> 0000_0000_1111_00_00_1111_10_00_1111_11_00
    def test_tx_phase_shift_concatenate_1(self):
        cv = ConvertingValues()

        tx0 = 357
        tx1 = 350
        tx2 = 340
        convert_value = cv.tx_phase_shift_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 15792380)

    # tx0 = 0, tx1 = 350, tx2 = 340 -> 0000_0000_1111_00_00_1111_10_00_0000_00_00
    def test_tx_phase_shift_concatenate_2(self):
        cv = ConvertingValues()

        tx0 = 0
        tx1 = 350
        tx2 = 340
        convert_value = cv.tx_phase_shift_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 15792128)

    # tx0 = 358, tx1 = 0, tx2 = 340 -> 0000_0000_1111_00_00_0000_00_00_1111_11_00
    def test_tx_phase_shift_concatenate_3(self):
        cv = ConvertingValues()

        tx0 = 357
        tx1 = 0
        tx2 = 340
        convert_value = cv.tx_phase_shift_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 15728892)

    # tx0 = 358, tx1 = 350, tx2 = 0 -> 0000_0000_0000_00_00_1111_10_00_1111_11_00
    def test_tx_phase_shift_concatenate_4(self):
        cv = ConvertingValues()

        tx0 = 357
        tx1 = 350
        tx2 = 0
        convert_value = cv.tx_phase_shift_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 63740)

    # tx0 = 0, tx1 = 0, tx2 = 0 -> 0000_0000_0000_00_00_0000_00_00_0000_00_00
    def test_tx_phase_shift_concatenate_5(self):
        cv = ConvertingValues()

        tx0 = 0
        tx1 = 0
        tx2 = 0
        convert_value = cv.tx_phase_shift_concatenate(tx0, tx1, tx2)

        self.assertEqual(convert_value, 0)

    # Перевод значения idle_time из мкс в деления
    def test_tx_start_time_converter_1(self):
        cv = ConvertingValues()

        value = 40.95
        convert_value = cv.tx_start_time_converter(value)

        self.assertEqual(convert_value, 4_095)

    # Перевод значения idle_time из мкс в деления
    def test_tx_start_time_converter_2(self):
        cv = ConvertingValues()

        value = -40.96
        convert_value = cv.tx_start_time_converter(value)

        self.assertEqual(convert_value, -4_096)

    # Перевод значения idle_time из мкс в деления
    def test_tx_start_time_converter_3(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.tx_start_time_converter(value)

        self.assertEqual(convert_value, 0)

    # Перевод частоты в деления
    # Деление = 53.644 Hz
    # Freq = 445.0 MHz
    # 445.0 MHz -> 445_000_000 Hz / 53.644 Hz ~ 8_295_429
    def test_start_freq_var_translation_1(self):
        cv = ConvertingValues()

        value = 445.0
        convert_value = cv.start_freq_var_translation(value)

        self.assertEqual(convert_value, 8_295_429)
        self.assertNotEqual(convert_value, 8_295_430)

    # Freq = 0 MHz
    # 0.0 MHz -> 0 Hz / 53.644 Hz ~ 0
    def test_start_freq_var_translation_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.start_freq_var_translation(value)

        self.assertEqual(convert_value, 0)

    # Перевод частоты в деления
    # Деление = 48.279 kHz/uS
    # Freq = 304.0 KHz/uS
    # 3040.0 KHz -> 304_000 kHz/uS / 48.279 kHz/uS ~ 63
    def test_freq_slope_var_translation_1(self):
        cv = ConvertingValues()

        value = 304.0
        convert_value = cv.freq_slope_var_translation(value)

        self.assertEqual(convert_value, 63)

    # Freq = 0 KHz/uS
    # 0 KHz -> 0 kHz/uS / 48.279 kHz/uS ~ 0
    def test_freq_slope_var_translation_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.freq_slope_var_translation(value)

        self.assertEqual(convert_value, 0)

    # Перевод периода в деления
    # Деление = 5 нс
    # 1.342 s -> 1_342_000_000 us -> 268_400_000
    def test_periodicity_translation_1(self):
        cv = ConvertingValues()

        value = 1342.0
        convert_value = cv.periodicity_translation(value)

        self.assertEqual(convert_value, 268_400_000)

    # 0 us -> 0
    def test_periodicity_translation_2(self):
        cv = ConvertingValues()

        value = 0
        convert_value = cv.periodicity_translation(value)

        self.assertEqual(convert_value, 0)

    # Перевод задержки в деления
    # Деление = 5 нс
    # 100.000 mcs -> 100_000 us / 5 us -> 20_000
    def test_delay_translation_1(self):
        cv = ConvertingValues()

        value = 100.0
        convert_value = cv.delay_translation(value)

        self.assertEqual(convert_value, 20_000)

    # 0.000 mcs -> 0 us / 5 us -> 0
    def test_delay_translation_2(self):
        cv = ConvertingValues()

        value = 0.0
        convert_value = cv.delay_translation(value)

        self.assertEqual(convert_value, 0)

    def test_position_code_convert_1(self):
        cv = ConvertingValues()

        v1 = True
        v2 = True
        v3 = False
        v4 = False

        convert_value = cv.position_code_convert(v1, v2, v3, v4)

        self.assertEqual(convert_value, 3)

    def test_position_code_convert_2(self):
        cv = ConvertingValues()

        v1 = True
        v2 = True
        v3 = True
        v4 = True

        convert_value = cv.position_code_convert(v1, v2, v3, v4)

        self.assertEqual(convert_value, 15)

    def test_position_code_convert_3(self):
        cv = ConvertingValues()

        v1 = True
        v2 = False
        v3 = True
        v4 = False

        convert_value = cv.position_code_convert(v1, v2, v3, v4)

        self.assertEqual(convert_value, 5)

    def test_position_code_convert_4(self):
        cv = ConvertingValues()

        v1 = False
        v2 = False
        v3 = False
        v4 = False

        convert_value = cv.position_code_convert(v1, v2, v3, v4)

        self.assertEqual(convert_value, 0)

    def test_position_code_convert_5(self):
        cv = ConvertingValues()

        v1 = False
        v2 = True
        v3 = False
        v4 = True

        convert_value = cv.position_code_convert(v1, v2, v3, v4)

        self.assertEqual(convert_value, 10)
