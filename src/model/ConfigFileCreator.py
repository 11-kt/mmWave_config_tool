import importlib.resources
import StringBuilder
import yaml
import gc

from model.ConvertingValues import ConvertingValues
from model.Data.Chirp import Chirp


class ConfigFileCreator:

    def __init__(self):
        self.cv: ConvertingValues = ConvertingValues()

        self.profile_dict: dict = {}
        self.chirp_dict: dict = {}
        self.data_param_dict: dict = {}
        self.frame_param_dict: dict = {}

        with importlib.resources.path("resources.mmwave_link", 'mmwaveconfig.txt') as path:
            self.config_file = path

        self.strings: dict = {}
        with importlib.resources.path("resources.strings", 'strings.yaml') as path:
            with open(path) as f:
                self.strings = yaml.safe_load(f)

    def create_config_file(self):
        self.write_base_config()

        self.write_available_profile()

        self.write_available_chirp()

        self.write_frame_config()

    def write_base_config(self):
        if len(self.data_param_dict) > 0:
            with open(self.config_file, 'w+') as f:
                f.write('# Base configuration\n')
                for key, value in self.data_param_dict.items():
                    sb = StringBuilder.StringBuilder()
                    sb.append(key)
                    sb.append('=')
                    sb.append(f'{value};\n')
                    f.write(sb.to_string())
            f.close()

    def write_available_profile(self):
        if len(self.profile_dict) > 0:
            with open(self.config_file, 'a') as f:
                for key, value in self.profile_dict.items():
                    sb = StringBuilder.StringBuilder()

                    sb.append(f'\n# Profile config {key} \n')

                    sb.append(self.strings['SignalConfigurationFrame']['profile'][2] + f'={value.id};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['start_freq'][2]
                              + f'={self.cv.start_freq_translation(value.start_freq)};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['idle_time'][2]
                              + f'={self.cv.idle_time_converter(value.idle_time)};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['adc_st'][2]
                              + f'={self.cv.adc_start_time_converter(value.adc_start_time)};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['ramp_et'][2]
                              + f'={self.cv.ramp_end_time_converter(value.ramp_end_time)};\n')

                    tx_pb = self.cv.tx_out_power_backoff_code_concatenate(
                        value.tx0_out_power_backoff_code,
                        value.tx1_out_power_backoff_code,
                        value.tx2_out_power_backoff_code
                    )
                    sb.append(self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][8]
                              + f'={tx_pb};\n')

                    ps = self.cv.tx_phase_shift_concatenate(0, 0, 0)
                    sb.append(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][4]
                              + f'={ps};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['freq_slope'][2]
                              + f'={self.cv.freq_slope_translation(value.freq_slope)};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['tx_Start_Time'][2]
                              + f'={self.cv.tx_start_time_converter(value.tx_start_time)};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['num_Adc_Samples_profile'][2]
                              + f'={value.adc_sample_rate};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['dig_Out_Sample_Rate'][2]
                              + f'={value.sample_rate};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][6]
                              + f'={value.hpf1_corner_freq};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][6]
                              + f'={value.hpf2_corner_freq};\n')

                    sb.append(self.strings['SignalConfigurationFrame']['rx_Gain'][2]
                              + f'={value.rx_gain};\n')

                    f.write(sb.to_string())

            f.close()

    def write_available_chirp(self):
        sub_dict = {}
        if len(self.chirp_dict) > 0:
            with open(self.config_file, 'a') as f:
                for key, value in self.chirp_dict.items():

                    if value.step != 0:
                        current_id = value.chirp_start_cfg_id - 1
                        for _ in range(int(value.last_chirp_idx / value.step)):
                            sb = StringBuilder.StringBuilder()

                            sb.append(f'\n# Chirp config {current_id}-{current_id} \n')

                            sb.append(self.strings['SignalConfigurationFrame']['chirp_Start_Idx'][2] +
                                      f'={current_id};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['chirp_End_Idx'][2] +
                                      f'={current_id};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['profile_Id'][2] +
                                      f'={value.profile_id};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['start_Freq_Var'][2] +
                                      f'={self.cv.start_freq_var_translation(value.start_freq_var)};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['freq_Slope_Var'][2] +
                                      f'={self.cv.freq_slope_var_translation(value.freq_slope_var)};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['idle_Time_Var'][2] +
                                      f'={self.cv.idle_time_converter(value.idle_time_var)};\n')

                            sb.append(self.strings['SignalConfigurationFrame']['adc_Start_Time_Var'][2] +
                                      f'={self.cv.adc_start_time_converter(value.adc_start_time_var)};\n')

                            tx_ena = self.cv.position_code_convert(
                                value.tx0,
                                value.tx1,
                                value.tx2,
                                False
                            )
                            sb.append(self.strings['SignalConfigurationFrame']['tx_Enable'][5] +
                                      f'={tx_ena};\n')

                            f.write(sb.to_string())

                            if current_id + value.step >= value.last_chirp_idx:
                                break
                            current_id += value.step

                            sub_dict[f'{current_id}, {current_id}'] = Chirp(
                                profile_id=value.profile_id,
                                chirp_start_cfg_id=current_id,
                                chirp_end_cfg_id=current_id,
                                start_freq_var=value.start_freq_var,
                                freq_slope_var=value.freq_slope_var,
                                idle_time_var=value.idle_time_var,
                                adc_start_time_var=value.adc_start_time_var,
                                enabled_tx=value.enabled_tx,
                                tx0=value.tx0,
                                tx1=value.tx1,
                                tx2=value.tx2,
                                step=value.step,
                                last_chirp_idx=value.last_chirp_idx
                            )

                    else:
                        sb = StringBuilder.StringBuilder()

                        sb.append(f'\n# Chirp config {value.chirp_start_cfg_id - 1}-{value.chirp_end_cfg_id - 1} \n')

                        sb.append(self.strings['SignalConfigurationFrame']['chirp_Start_Idx'][2] +
                                  f'={value.chirp_start_cfg_id - 1};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['chirp_End_Idx'][2] +
                                  f'={value.chirp_end_cfg_id - 1};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['profile_Id'][2] +
                                  f'={value.profile_id};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['start_Freq_Var'][2] +
                                  f'={self.cv.start_freq_var_translation(value.start_freq_var)};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['freq_Slope_Var'][2] +
                                  f'={self.cv.freq_slope_var_translation(value.freq_slope_var)};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['idle_Time_Var'][2] +
                                  f'={self.cv.idle_time_converter(value.idle_time_var)};\n')

                        sb.append(self.strings['SignalConfigurationFrame']['adc_Start_Time_Var'][2] +
                                  f'={self.cv.adc_start_time_converter(value.adc_start_time_var)};\n')

                        tx_ena = self.cv.position_code_convert(
                            value.tx0,
                            value.tx1,
                            value.tx2,
                            False
                        )
                        sb.append(self.strings['SignalConfigurationFrame']['tx_Enable'][5] +
                                  f'={tx_ena};\n')

                        f.write(sb.to_string())
            for key, value in sub_dict.items():
                self.chirp_dict[key] = value
                f.close()

    def write_frame_config(self):
        if len(self.frame_param_dict) > 0:
            with open(self.config_file, 'a') as f:
                f.write('\n# Frame configuration\n')
                for key, value in self.frame_param_dict.items():
                    sb = StringBuilder.StringBuilder()
                    sb.append(key)
                    sb.append('=')
                    sb.append(f'{value};\n')
                    f.write(sb.to_string())
            f.close()

    def clear_data(self):
        del self.profile_dict
        del self.chirp_dict
        del self.data_param_dict
        del self.frame_param_dict

        gc.collect()

        self.profile_dict: dict = {}
        self.chirp_dict: dict = {}
        self.data_param_dict: dict = {}
        self.frame_param_dict: dict = {}
