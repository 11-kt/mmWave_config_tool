from dataclasses import dataclass


@dataclass
class Chirp:
    profile_id: int
    chirp_start_cfg_id: int
    chirp_end_cfg_id: int
    start_freq_var: float
    freq_slope_var: float
    idle_time_var: float
    adc_start_time_var: float
    enabled_tx: int
    tx0: bool
    tx1: bool
    tx2: bool
    step: int
    last_chirp_idx: int
