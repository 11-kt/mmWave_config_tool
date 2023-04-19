from StringBuilder.string_builder import StringBuilder


class ConvertingValues:

    # Для AWR1243 допустимый диапазон = 76-81GHz
    # В конфигурационный файл передается кол-во делений
    # 1 LSB = 3.6e9 / 2^26 Hz = 53.644 Hz
    # Valid range: 0x5471C71B to 0x5A000000
    def start_freq_translation(self, freq):
        lsb = 53.644

        max_value = 1_509_949_440

        freq_hz = self.convert_ghz_hz(freq)
        res = round(freq_hz / lsb)

        return res if res < max_value else max_value

    # Максимальный уклон для сенсора AWR1243 = 100 MHz/uS
    # В конфигурационный файл передается кол-во делений
    # 1 LSB = (3.6e6 * 900) / 2^26 = 48.279 kHz/uS
    # Valid range: -2072 to 2072 (Max 100MHz/uS)
    def freq_slope_translation(self, freq_slope):
        lsb = 48.279

        freq_khz = self.convert_mhz_khz(freq_slope)

        return round(freq_khz / lsb)

    # Конвертация idle time (мкс) в нс
    # 1 LSB = 10 ns
    @staticmethod
    def idle_time_converter(idle_time):
        return int(idle_time * 100)

    # Конвертация adc_start_time (мкс) в нс
    # 1 LSB = 10 ns
    @staticmethod
    def adc_start_time_converter(adc_st):
        return int(adc_st * 100)

    # Конвертация ramp end time (мкс) в нс
    # 1 LSB = 10 ns
    @staticmethod
    def ramp_end_time_converter(ramp_et):
        return int(ramp_et * 100)

    # Объединение значений tx0-tx2 out power backoff code
    # b7:0 TX0 output power back off
    # b15:8 TX1 output power back off
    # b23:16 TX2 output power back off
    # b31:24 Reserved
    @staticmethod
    def tx_out_power_backoff_code_concatenate(tx0, tx1, tx2):
        sb = StringBuilder()

        sb.append('00000000')

        sb.append('{0:08b}'.format(tx2))

        sb.append('{0:08b}'.format(tx1))

        sb.append('{0:08b}'.format(tx0))

        return sb.to_string()

    # Объединение значений tx0-tx2 phase shift
    # 1 LSB = 360/2^6 = 5.625 degrees
    # b1:0 Reserved (set to 0b00)
    # b7:2 TX0 phase shift value
    # b9:8 Reserved (set to 0b00)
    # b15:10 TX1 phase shift value
    # b17:16 Reserved (set to 0b00)
    # b23:18 TX2 phase shift value
    # b31:24 Reserved
    @staticmethod
    def tx_phase_shift_concatenate(tx0, tx1, tx2):
        sb = StringBuilder()

        lsb = 5.625

        sb.append('00000000')

        sb.append('{0:06b}'.format(round(tx2 / lsb)))

        sb.append('00')

        sb.append('{0:06b}'.format(round(tx1 / lsb)))

        sb.append('00')

        sb.append('{0:06b}'.format(round(tx0 / lsb)))

        sb.append('00')

        return sb.to_string()

    # Конвертация tx start time (мкс) в нс
    # 1 LSB = 10 ns
    @staticmethod
    def tx_start_time_converter(tx_start_time):
        return int(tx_start_time * 100)

    # Максимальное значение = 449.9 MHz
    # 1 LSB = 3.6e9/2^26 = 53.644 Hz
    # valid range = 0-8388607
    def start_freq_var_translation(self, freq):
        lsb = 53.644

        max_value = 8_388_607

        freq_hz = self.convert_mhz_hz(freq)
        res = round(freq_hz / lsb)

        return res if res < max_value else max_value

    # Максимальный уклон для сенсора AWR1243 = 3041,577 KHz/uS
    # 1 LSB = (3.6e6 * 900) / 2^26 = 48.279 kHz/uS
    # Valid range: 0 to 63
    def freq_slope_var_translation(self, freq_slope):
        lsb = 48.279

        freq_khz = self.convert_mhz_khz(freq_slope)

        return round(freq_khz / lsb / 100)

    # конвертация периода из ms в us
    # 1 LSB = 5 ns
    # Valid range : 300 us to 1.342 s
    def periodicity_translation(self, period):
        lsb = 5

        period_us = self.convert_ms_ns(period)

        return round(period_us / lsb)

    # конвертация задержки из mсs в us
    # 1 LSB = 5 ns
    # Typical range is 0 to 100 micro seconds
    def delay_translation(self, delay):
        lsb = 5

        delay_us = self.convert_mcs_ns(delay)

        return round(delay_us / lsb)

    # ms to us converter
    @staticmethod
    def convert_ms_ns(period):
        return period * 10**6

    # mcs to us converter
    @staticmethod
    def convert_mcs_ns(period):
        return period * 10**3

    # GHz to Hz converter
    @staticmethod
    def convert_ghz_hz(freq):
        return freq * 10**9

    # MHz to kHz converter
    @staticmethod
    def convert_mhz_khz(freq):
        return freq * 10**3

    # GHz to Hz converter
    @staticmethod
    def convert_mhz_hz(freq):
        return freq * 10**6
