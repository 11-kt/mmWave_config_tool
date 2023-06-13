from dataclasses import dataclass


@dataclass
class Profile:
    id: int
    start_freq: float
    freq_slope: float
    idle_time: float
    adc_start_time: float
    ramp_end_time: float
    tx0_out_power_backoff_code: int
    tx1_out_power_backoff_code: int
    tx2_out_power_backoff_code: int
    tx_start_time: float
    adc_sample_rate: int
    sample_rate: int
    hpf1_corner_freq: int
    hpf2_corner_freq: int
    rx_gain: int

