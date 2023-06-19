import os
import subprocess
import sys
import importlib.resources
import yaml
import asyncio

from PyQt6.QtWidgets import QFileDialog

from view.windows.MainWindow import MainWindow

from model.ConfigFileCreator import ConfigFileCreator
from model.ConvertingValues import ConvertingValues
from model.PostProc.PostProc import PostProc
from model.JsonWriter import *
from model.Data.Profile import Profile
from model.Data.Chirp import Chirp
from model.Resolutions.AngleResolution import angle_resolution
from model.Resolutions.RangeResolution import *


class MainWindowController:

    def __init__(self):

        # Main Window
        self.window = MainWindow()
        self.window.main_layout.addWidget(self.window.start_frame)
        self.window.show()

        # First signal config stage
        self.signal_config_stage_flag: bool = False

        # Profile and Chirp conf stage done
        self.is_Prof_Chirp: bool = False

        # Configuration File Creator
        self.conf_file_creator: ConfigFileCreator = ConfigFileCreator()

        # Converter values
        self.converter: ConvertingValues = ConvertingValues()

        # Plot result
        self.plotter = None

        # Coroutines
        self.ioloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.is_mmwave_link_done: bool = False
        self.is_been_configured: bool = False

        self.strings: dict = {}
        with importlib.resources.path("resources.strings", 'strings.yaml') as path:
            with open(path) as f:
                self.strings = yaml.safe_load(f)

        self.error_codes: dict = {}
        with importlib.resources.path("resources.strings", 'error_codes.yaml') as path:
            with open(path) as f:
                self.error_codes = yaml.safe_load(f)

        with importlib.resources.path("resources.cli_control", 'cf.json') as path:
            self.cli_config_json = path

        with importlib.resources.path("resources.cli_control", 'DCA1000EVM_CLI_Control.exe') as path:
            self.cli_control_exe = path

        with importlib.resources.path("resources.cli_control", 'DCA1000EVM_CLI_Record.exe') as path:
            self.cli_record_exe = path

        with importlib.resources.path("resources.mmwave_link", "mmwavelink.exe") as path:
            self.mmwave_link_exe = path

    def data_path_configuration_slot(self):
        if self.window.start_frame.data_Path_cb.currentData() == 0:
            self.window.start_frame.lane_CLK_cb.model().item(1).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(0).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(1).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(2).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(3).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(4).setEnabled(True)
            self.window.start_frame.data_Rate_cb.model().item(5).setEnabled(True)
        else:
            self.window.start_frame.lane_CLK_cb.setCurrentIndex(0)
            self.window.start_frame.lane_CLK_cb.model().item(1).setEnabled(False)

            self.window.start_frame.data_Rate_cb.setCurrentIndex(0)
            self.window.start_frame.data_Rate_cb.model().item(0).setEnabled(False)
            self.window.start_frame.data_Rate_cb.model().item(2).setEnabled(False)
            self.window.start_frame.data_Rate_cb.model().item(4).setEnabled(False)
            self.window.start_frame.data_Rate_cb.model().item(5).setEnabled(False)

    def num_adc_sample_range_slot(self):
        curr_data_format = self.window.start_frame.adc_Format_cb.currentData()

        curr_rx_enabled = self.window.start_frame.Rx0_cb.isChecked() + self.window.start_frame.Rx1_cb.isChecked() + \
                          self.window.start_frame.Rx2_cb.isChecked() + self.window.start_frame.Rx3_cb.isChecked()

        if (curr_data_format == 0 or curr_data_format == 3) and curr_rx_enabled == 4:
            self.window.signal_conf_frame.num_Adc_Samples_profile_sb.setMaximum(2048)

        if (curr_data_format == 1 or curr_data_format == 2) and curr_rx_enabled == 4:
            self.window.signal_conf_frame.num_Adc_Samples_profile_sb.setMaximum(1024)

        if (curr_data_format == 0 or curr_data_format == 3) and curr_rx_enabled == 2:
            self.window.signal_conf_frame.num_Adc_Samples_profile_sb.setMaximum(4096)

        if (curr_data_format == 1 or curr_data_format == 2) and curr_rx_enabled == 2:
            self.window.signal_conf_frame.num_Adc_Samples_profile_sb.setMaximum(2048)

    def num_adc_sample_rate_slot(self):
        curr_value = self.window.start_frame.adc_Format_cb.currentData()

        if curr_value == 0 or curr_value == 3:
            self.window.signal_conf_frame.num_Adc_Samples_frame_sb.setValue(
                self.window.signal_conf_frame.num_Adc_Samples_profile_sb.value()
            )

        else:
            self.window.signal_conf_frame.num_Adc_Samples_frame_sb.setValue(
                2 * self.window.signal_conf_frame.num_Adc_Samples_profile_sb.value()
            )

    def tx_controller_slot(self):
        is_tx0 = self.window.start_frame.Tx0_sb.isChecked()
        is_tx1 = self.window.start_frame.Tx1_sb.isChecked()
        is_tx2 = self.window.start_frame.Tx2_sb.isChecked()

        if is_tx0 and not (is_tx1 and is_tx2):
            self.window.signal_conf_frame.tx0_en_cb.setChecked(True)

            self.window.signal_conf_frame.tx1_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx1_en_cb.setEnabled(False)

            self.window.signal_conf_frame.tx2_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx2_en_cb.setEnabled(False)

        if is_tx1 and not (is_tx0 and is_tx2):
            self.window.signal_conf_frame.tx1_en_cb.setChecked(True)

            self.window.signal_conf_frame.tx0_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx0_en_cb.setEnabled(False)

            self.window.signal_conf_frame.tx2_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx2_en_cb.setEnabled(False)

        if is_tx2 and not (is_tx0 and is_tx1):
            self.window.signal_conf_frame.tx2_en_cb.setChecked(True)

            self.window.signal_conf_frame.tx1_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx1_en_cb.setEnabled(False)

            self.window.signal_conf_frame.tx0_en_cb.setChecked(False)
            self.window.signal_conf_frame.tx0_en_cb.setEnabled(False)

        if is_tx0 and is_tx1:
            self.window.start_frame.Tx2_sb.setEnabled(False)

            self.window.signal_conf_frame.tx0_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx0_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx1_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx1_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx2_en_cb.setChecked(False)

        else:
            self.window.start_frame.Tx2_sb.setEnabled(True)

        if is_tx0 and is_tx2:
            self.window.start_frame.Tx1_sb.setEnabled(False)

            self.window.signal_conf_frame.tx0_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx0_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx2_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx2_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx1_en_cb.setChecked(False)

        else:
            self.window.start_frame.Tx1_sb.setEnabled(True)

        if is_tx1 and is_tx2:
            self.window.start_frame.Tx0_sb.setEnabled(False)

            self.window.signal_conf_frame.tx1_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx1_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx2_en_cb.setChecked(True)
            self.window.signal_conf_frame.tx2_en_cb.setEnabled(True)

            self.window.signal_conf_frame.tx0_en_cb.setChecked(False)

        else:
            self.window.start_frame.Tx0_sb.setEnabled(True)

    def angle_resolution_slot(self):
        tx = self.window.start_frame.Tx0_cb.isChecked() + \
             self.window.start_frame.Tx1_cb.isChecked() + \
             self.window.start_frame.Tx2_cb.isChecked()

        rx = self.window.start_frame.Rx0_cb.isChecked() + \
             self.window.start_frame.Rx1_cb.isChecked() + \
             self.window.start_frame.Rx2_cb.isChecked() + \
             self.window.start_frame.Rx3_cb.isChecked()

        if tx != 0 and rx != 0:
            degree_resolution, _ = angle_resolution(tx, rx)

            self.window.start_frame.degree_val_label.setText(str(round(degree_resolution, 4)))

    def bandwidth_change_slot(self):
        curr_bandwidth = bandwidth(
            freq_slope=self.window.signal_conf_frame.freq_slope_sb.value(),
            sample_rate=self.window.signal_conf_frame.dig_Out_Sample_Rate_sb.value(),
            adc_sample_rate=self.window.signal_conf_frame.num_Adc_Samples_profile_sb.value()
        )

        self.window.signal_conf_frame.bandwidth_val_label.setText(str(round(curr_bandwidth / 1e6, 4)))

        if curr_bandwidth != 0:
            curr_range_resolution = range_res(curr_bandwidth)
            self.window.signal_conf_frame.range_resolution_val_label.setText(str(round(curr_range_resolution, 6)))

        else:
            self.window.signal_conf_frame.range_resolution_val_label.setText(
                self.strings['SignalConfigurationFrame']['range_resolution'][2]
            )

    def iq_swap_slot(self):
        if self.window.start_frame.adc_Format_cb.currentData() in [0, 3]:
            self.window.start_frame.iq_swap_cb.setCurrentIndex(0)
            self.window.start_frame.iq_swap_cb.setEnabled(False)

        else:
            self.window.start_frame.iq_swap_cb.setCurrentIndex(0)
            self.window.start_frame.iq_swap_cb.setEnabled(True)

    def configurate_profile_slot(self):
        profile = Profile(
            id=self.window.signal_conf_frame.profile_sb.value(),
            start_freq=self.window.signal_conf_frame.start_freq_sb.value(),
            freq_slope=self.window.signal_conf_frame.freq_slope_sb.value(),
            idle_time=self.window.signal_conf_frame.idle_time_sb.value(),
            adc_start_time=self.window.signal_conf_frame.adc_st_sb.value(),
            ramp_end_time=self.window.signal_conf_frame.ramp_et_sb.value(),
            tx0_out_power_backoff_code=self.window.signal_conf_frame.tx0_Out_Power_Backoff_Code_cb.currentData(),
            tx1_out_power_backoff_code=self.window.signal_conf_frame.tx1_Out_Power_Backoff_Code_cb.currentData(),
            tx2_out_power_backoff_code=self.window.signal_conf_frame.tx2_Out_Power_Backoff_Code_cb.currentData(),
            tx_start_time=self.window.signal_conf_frame.tx_Start_Time_sb.value(),
            adc_sample_rate=self.window.signal_conf_frame.num_Adc_Samples_profile_sb.value(),
            sample_rate=self.window.signal_conf_frame.dig_Out_Sample_Rate_sb.value(),
            hpf1_corner_freq=self.window.signal_conf_frame.hpf_Corner_Freq1_cb.currentData(),
            hpf2_corner_freq=self.window.signal_conf_frame.hpf_Corner_Freq2_cb.currentData(),
            rx_gain=self.window.signal_conf_frame.rx_Gain_cb.currentData()
        )

        self.conf_file_creator.profile_dict[profile.id] = profile

        self.window.signal_conf_frame.set_chirp_button.setEnabled(True)
        self.window.signal_conf_frame.profile_Id_cb.model().item(profile.id).setEnabled(True)

    def configurate_chirp_slot(self):
        chirp = Chirp(
            profile_id=self.window.signal_conf_frame.profile_Id_cb.currentData(),
            chirp_start_cfg_id=self.window.signal_conf_frame.chirp_Start_Idx_sb.value(),
            chirp_end_cfg_id=self.window.signal_conf_frame.chirp_End_Idx_sb.value(),
            start_freq_var=self.window.signal_conf_frame.start_Freq_Var_sb.value(),
            freq_slope_var=self.window.signal_conf_frame.freq_Slope_Var_sb.value(),
            idle_time_var=self.window.signal_conf_frame.idle_Time_Var_sb.value(),
            adc_start_time_var=self.window.signal_conf_frame.adc_Start_Time_Var_sb.value(),
            enabled_tx=self.window.signal_conf_frame.tx0_en_cb.isChecked() +
                       self.window.signal_conf_frame.tx1_en_cb.isChecked() +
                       self.window.signal_conf_frame.tx2_en_cb.isChecked(),
            tx0=self.window.signal_conf_frame.tx0_en_cb.isChecked(),
            tx1=self.window.signal_conf_frame.tx1_en_cb.isChecked(),
            tx2=self.window.signal_conf_frame.tx2_en_cb.isChecked(),
            step=self.window.signal_conf_frame.set_step_sb.value(),
            last_chirp_idx=self.window.signal_conf_frame.set_idx_sb.value()
        )

        self.conf_file_creator.chirp_dict[f'{chirp.chirp_start_cfg_id}, {chirp.chirp_end_cfg_id}'] = chirp

        self.is_Prof_Chirp = True

    def step_chirp_slot(self):
        if self.window.signal_conf_frame.chirp_Start_Idx_sb.value() == \
                self.window.signal_conf_frame.chirp_End_Idx_sb.value():
            self.window.signal_conf_frame.set_step_sb.setEnabled(True)
            self.window.signal_conf_frame.set_idx_sb.setEnabled(True)

        else:
            self.window.signal_conf_frame.set_step_sb.setValue(0)
            self.window.signal_conf_frame.set_step_sb.setEnabled(False)
            self.window.signal_conf_frame.set_idx_sb.setValue(1)
            self.window.signal_conf_frame.set_idx_sb.setEnabled(False)

    @staticmethod
    def open_log_file_in_notepad_slot():
        with importlib.resources.path("resources.mmwave_link", "log.txt") as path:
            os.startfile(str(path))

    def back_to_start_slot(self):
        self.window.signal_conf_frame.hide()
        self.window.start_frame.show()

    def back_to_signal_conf_slot(self):
        self.plotter.clear_data()
        self.conf_file_creator.clear_data()

        self.window.wait_frame.hide()
        self.window.signal_conf_frame.show()

        self.window.rebuild_wait_frame()
        self.wait_frame_signals()

    def file_path_browse_slot(self):
        path = QFileDialog.getExistingDirectory()

        if path != '':
            self.window.signal_conf_frame.result_path_browser.setText(path)

        else:
            self.window.signal_conf_frame.result_path_browser.setStyleSheet('QLineEdit { background-color: red }')

    def plot_type_pick_slot(self):
        if self.window.result_frame.plot_type_cb.currentData() in [5, 8]:
            self.window.result_frame.cfar_config_gb.show()

        elif self.window.result_frame.plot_type_cb.currentData() == 3:
            self.window.result_frame.chirp_pick_sb.setDisabled(True)

        else:
            self.window.result_frame.chirp_pick_sb.setDisabled(False)
            self.window.result_frame.cfar_config_gb.hide()

    def re_configurate_slot(self):
        self.plotter.clear_data()
        self.conf_file_creator.clear_data()

        self.window.result_frame.hide()
        self.window.start_frame.show()

        self.window.rebuild_wait_frame()
        self.wait_frame_signals()

        self.window.rebuild_result_frame()
        self.result_frame_signals()

    def fill_param_dict_start_frame(self):
        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cascading_Mode'][5]] = 0

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['crcType'][0]] = \
            int(self.window.start_frame.crc_cb.isChecked())

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['ackTimeout'][0]] = 50000

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['channel_Tx'][5]] = \
            self.converter.position_code_convert(
                self.window.start_frame.Tx0_cb.isChecked(),
                self.window.start_frame.Tx1_cb.isChecked(),
                self.window.start_frame.Tx2_cb.isChecked(),
                False
            )

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['channel_Rx'][6]] = \
            self.converter.position_code_convert(
                self.window.start_frame.Rx0_cb.isChecked(),
                self.window.start_frame.Rx1_cb.isChecked(),
                self.window.start_frame.Rx2_cb.isChecked(),
                self.window.start_frame.Rx3_cb.isChecked()
            )

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cascading_Mode'][6]] = 0

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['adc_Bits'][5]] = \
            self.window.start_frame.adc_Bits_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['adc_Format'][6]] = \
            self.window.start_frame.adc_Format_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['channel_Rx'][7]] = \
            self.converter.position_code_convert(
                self.window.start_frame.Rx0_cb.isChecked(),
                self.window.start_frame.Rx1_cb.isChecked(),
                self.window.start_frame.Rx2_cb.isChecked(),
                self.window.start_frame.Rx3_cb.isChecked()
            )

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['adc_Bits'][6]] = \
            self.window.start_frame.adc_Bits_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['adc_Format'][7]] = \
            1 if self.window.start_frame.adc_Format_cb.currentData() in [1, 2] else 0

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['iqSwapSel'][3]] = \
            self.window.start_frame.iq_swap_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['chInterleave'][0]] = 0

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['lp_Adc_Mode'][4]] = \
            self.window.start_frame.lp_Adc_Mode_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['data_Path'][5]] = 1

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['Pkt0'][6]] = \
            self.window.start_frame.Pkt0_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['Pkt1'][5]] = \
            self.window.start_frame.Pkt1_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cq_conf'][5]] = \
            self.window.start_frame.cq_conf_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cq0'][2]] = \
            self.window.start_frame.cq0_sb.value()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cq1'][2]] = \
            self.window.start_frame.cq1_sb.value()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['cq2'][2]] = \
            self.window.start_frame.cq2_sb.value()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['lane_CLK'][4]] = \
            self.window.start_frame.lane_CLK_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['data_Rate'][8]] = \
            self.window.start_frame.data_Rate_cb.currentData()[0]

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['data_Rate'][9]] = \
            self.window.start_frame.data_Rate_cb.currentData()[1]

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['lane_conf'][6]] = \
            self.converter.position_code_convert(
                self.window.start_frame.lane1_cb.isChecked(),
                self.window.start_frame.lane2_cb.isChecked(),
                self.window.start_frame.lane3_cb.isChecked(),
                self.window.start_frame.lane4_cb.isChecked()
            )

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['lane_Format'][4]] = \
            self.window.start_frame.lane_Format_cb.currentData()

        self.conf_file_creator.data_param_dict[self.strings['StartFrame']['lane_param_conf'][8]] = \
            self.converter.position_code_convert(
                self.window.start_frame.msb_first_cb.isChecked(),
                self.window.start_frame.crc_cb.isChecked(),
                False,
                False
            )

    def fill_param_dict_signal_conf_frame(self):

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['chirp_Start_Id'][2]] = \
            self.window.signal_conf_frame.chirp_Start_Id_sb.value() - 1

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['chirp_End_Id'][2]] = \
            self.window.signal_conf_frame.chirp_End_Id_sb.value() - 1

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['frame_Count'][2]] = \
            self.window.signal_conf_frame.frame_Count_sb.value()

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['loop_Count'][2]] = \
            self.window.signal_conf_frame.loop_Count_sb.value()

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['periodicity'][2]] = \
            self.converter.periodicity_translation(self.window.signal_conf_frame.periodicity_sb.value())

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['trigger_Delay'][2]] = \
            self.converter.delay_translation(self.window.signal_conf_frame.trigger_Delay_sb.value())

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['num_Adc_Samples_frame'][2]] =\
            self.window.signal_conf_frame.num_Adc_Samples_frame_sb.value()

        self.conf_file_creator.frame_param_dict[self.strings['SignalConfigurationFrame']['trigger_Select'][4]] = \
            self.window.signal_conf_frame.trigger_Select_cb.currentData()

    def signal_conf_stage(self):
        self.fill_param_dict_start_frame()
        self.window.start_frame.hide()

        if not self.signal_config_stage_flag:
            self.window.main_layout.addWidget(self.window.signal_conf_frame)
            self.signal_config_stage_flag = True

        else:
            self.window.signal_conf_frame.show()

    def start_device_stage(self):
        self.fill_param_dict_signal_conf_frame()
        self.window.signal_conf_frame.hide()

        self.window.main_layout.addWidget(self.window.wait_frame)

        self.is_been_configured = True

        self.conf_file_creator.create_config_file()

        self.ioloop.run_in_executor(None, self.start_record_data)

        self.ioloop.run_in_executor(None, self.start_mmwave_link)

    def result_plot_stage(self):
        self.window.wait_frame.hide()
        self.window.main_layout.addWidget(self.window.result_frame)

    def write_csv_file(self):
        self.ioloop.run_in_executor(None, self.plotter.write_csv_data)

    def start_record_data(self):

        update_json_file_path_mode(self.window.signal_conf_frame.result_path_browser.text())

        num_chirps = self.window.signal_conf_frame.chirp_End_Id_sb.value() - \
                     self.window.signal_conf_frame.chirp_Start_Id_sb.value() + 1

        update_json_capture_config(
            num_frames=self.window.signal_conf_frame.frame_Count_sb.value(),
            num_loops=self.window.signal_conf_frame.loop_Count_sb.value(),
            num_chirps=num_chirps,
            num_samples=self.window.signal_conf_frame.num_Adc_Samples_frame_sb.value()
        )

        result_code = subprocess.call([str(self.cli_record_exe), 'start_record', str(self.cli_config_json)])

        if result_code == 0 and self.is_mmwave_link_done:
            self.configurate_post_proc()
            self.plotter.organize_data_by_lane()
            self.plotter.organize_data_per_frame_loop_chirp_antenna_sample()
            self.configurate_result_frame()
            self.window.wait_frame.csv_create_button.setDisabled(False)
            self.window.wait_frame.next_button.setDisabled(False)
            self.is_mmwave_link_done = False

            self.window.wait_frame.wait_gif_label.hide()
            self.window.wait_frame.successfully_img.show()
            self.window.wait_frame.info_label.setText(self.strings['WaitFrame']['label'][1])

        self.window.wait_frame.exit_button.setDisabled(False)
        self.window.wait_frame.back_button.setDisabled(False)

    def start_mmwave_link(self):

        download_firmware = str(int(self.window.start_frame.firmware_cb.isChecked()))
        num_frames = str(self.window.signal_conf_frame.frame_Count_sb.value())

        with importlib.resources.path("resources.mmwave_link", "mmwaveconfig.txt") as path:
            log_file = str(path).removesuffix("mmwaveconfig.txt") + "log.txt"

            with open(log_file, "wb") as f:
                process = subprocess.Popen([
                    str(self.mmwave_link_exe),
                    download_firmware,
                    num_frames,
                    str(path)
                ],
                    stdout=subprocess.PIPE)
                process.wait()

                for line in iter(process.stdout.readline, b""):
                    f.write(line)
            return_code = process.returncode

            if return_code != 0:
                self.window.wait_frame.next_button.hide()
                self.window.wait_frame.open_log_button.show()

                self.window.wait_frame.wait_gif_label.hide()
                self.window.wait_frame.error_img.show()
                self.window.wait_frame.info_label.setText(
                    self.strings['Controller'][0] +
                    f'{return_code}\n' +
                    self.error_codes[return_code][0]
                )

            else:
                self.is_mmwave_link_done = True

    def connection_check_button(self):
        self.ioloop.run_in_executor(None, self.check_connection_status)

    def check_connection_status(self):
        self.window.signal_conf_frame.exit_button.setDisabled(True)
        self.window.signal_conf_frame.connection_check_button.setDisabled(True)

        update_json_data_format_mode(self.window.start_frame.adc_Bits_cb.currentData() + 1)

        result_code = subprocess.call([str(self.cli_control_exe), 'fpga_version', str(self.cli_config_json)])

        self.window.signal_conf_frame.neutral_connection_status.hide()

        if result_code == 1026:
            self.window.signal_conf_frame.unsuccessful_connection_status.hide()
            self.window.signal_conf_frame.config_fpga_path_button.setDisabled(False)
            self.window.signal_conf_frame.successful_connection_status.show()

        else:
            self.window.signal_conf_frame.successful_connection_status.hide()
            self.window.signal_conf_frame.unsuccessful_connection_status.show()

        self.window.signal_conf_frame.exit_button.setDisabled(False)
        self.window.signal_conf_frame.connection_check_button.setDisabled(False)

    def fpga_path_configuration_button(self):
        self.ioloop.run_in_executor(None, self.fpga_path_configuration)

    def fpga_path_configuration(self):
        self.window.signal_conf_frame.exit_button.setDisabled(True)
        self.window.signal_conf_frame.config_fpga_path_button.setDisabled(True)

        result_code = subprocess.call([str(self.cli_control_exe), 'fpga', str(self.cli_config_json)])

        self.window.signal_conf_frame.config_status.hide()

        if result_code == 0:
            self.window.signal_conf_frame.successful_config_status.show()
            if self.is_Prof_Chirp:
                self.window.signal_conf_frame.next_button.setDisabled(False)

        else:
            self.window.signal_conf_frame.unsuccessful_config_status.show()

        self.window.signal_conf_frame.exit_button.setDisabled(False)

    def file_path_edit_signal(self):
        if os.path.isdir(self.window.signal_conf_frame.result_path_browser.text()):
            self.window.signal_conf_frame.result_path_browser.setStyleSheet('QLineEdit { background-color: white }')

        else:
            self.window.signal_conf_frame.result_path_browser.setStyleSheet('QLineEdit { background-color: red }')

    def configurate_post_proc(self):
        data_type = True
        if self.window.start_frame.adc_Format_cb.currentData() in [1, 2]:
            data_type = False

        adc_bits = 16
        if self.window.start_frame.adc_Bits_cb.currentData() == 0:
            adc_bits = 12
        if self.window.start_frame.adc_Bits_cb.currentData() == 1:
            adc_bits = 14
        tx = 1
        if self.window.start_frame.Tx0_sb.isChecked() and self.window.start_frame.Tx1_sb.isChecked():
            tx = 2
        if self.window.start_frame.Tx0_sb.isChecked() and self.window.start_frame.Tx2_sb.isChecked():
            tx = 2
        if self.window.start_frame.Tx1_sb.isChecked() and self.window.start_frame.Tx2_sb.isChecked():
            tx = 2
        self.plotter = PostProc(
            profile_dict=self.conf_file_creator.profile_dict,
            chirp_dict=self.conf_file_creator.chirp_dict,
            tx_ena=tx,
            rx_ena=self.window.start_frame.Rx0_cb.isChecked() + self.window.start_frame.Rx1_cb.isChecked() +
                   self.window.start_frame.Rx2_cb.isChecked() + self.window.start_frame.Rx3_cb.isChecked(),
            adc_bits=adc_bits,
            path=self.window.signal_conf_frame.result_path_browser.text() + '\\adc_data_Raw_0.bin',
            data_type=data_type,
            num_frames=self.window.signal_conf_frame.frame_Count_sb.value(),
            num_loops=self.window.signal_conf_frame.loop_Count_sb.value(),
            num_chirps=self.window.signal_conf_frame.chirp_End_Id_sb.value(),
        )

        # If real -> image plot unavailable
        if data_type:
            self.window.result_frame.plot_type_cb.model().item(2).setEnabled(False)

        else:
            self.window.result_frame.plot_type_cb.model().item(2).setEnabled(True)

        # available lane control
        lane4 = self.window.start_frame.lane4_cb.isChecked()
        if not lane4:
            self.window.result_frame.lane_pick_cb.model().item(3).setEnabled(False)
        else:
            self.window.result_frame.lane_pick_cb.model().item(3).setEnabled(True)
            self.window.result_frame.lane_pick_cb.setCurrentIndex(3)

        lane3 = self.window.start_frame.lane3_cb.isChecked()
        if not lane3:
            self.window.result_frame.lane_pick_cb.model().item(2).setEnabled(False)
        else:
            self.window.result_frame.lane_pick_cb.model().item(2).setEnabled(True)
            self.window.result_frame.lane_pick_cb.setCurrentIndex(2)

        lane2 = self.window.start_frame.lane2_cb.isChecked()
        if not lane2:
            self.window.result_frame.lane_pick_cb.model().item(1).setEnabled(False)
        else:
            self.window.result_frame.lane_pick_cb.model().item(1).setEnabled(True)
            self.window.result_frame.lane_pick_cb.setCurrentIndex(1)

        lane1 = self.window.start_frame.lane1_cb.isChecked()
        if not lane1:
            self.window.result_frame.lane_pick_cb.model().item(0).setEnabled(False)
        else:
            self.window.result_frame.lane_pick_cb.model().item(0).setEnabled(True)
            self.window.result_frame.lane_pick_cb.setCurrentIndex(0)

    def configurate_result_frame(self):
        self.window.result_frame.frame_pick_sb.setRange(1, self.window.signal_conf_frame.frame_Count_sb.value())
        self.window.result_frame.chirp_pick_sb.setRange(1, self.window.signal_conf_frame.chirp_End_Id_sb.value())
        self.window.result_frame.loop_pick_sb.setRange(1, self.window.signal_conf_frame.loop_Count_sb.value())

    def plot_result(self):

        plot_type = self.window.result_frame.plot_type_cb.currentData()

        frame_id = self.window.result_frame.frame_pick_sb.value() - 1

        loop_id = self.window.result_frame.loop_pick_sb.value() - 1

        chirp_id = self.window.result_frame.chirp_pick_sb.value() - 1

        lane_id = self.window.result_frame.lane_pick_cb.currentData()

        self.window.result_frame.mplc_2d.axes.clear()
        self.window.result_frame.mplc_3d.axes.clear()

        if plot_type == 0:
            self.plotter.fft_1d_plot(frame_id, loop_id, chirp_id, lane_id, 2)

            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[1])
            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['RangeFFT'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['RangeFFT'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['RangeFFT'][2])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 1:
            self.plotter.fft_1d_plot(frame_id, loop_id, chirp_id, lane_id, 0)

            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[1])
            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['RangeFFT'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['RangeFFT'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['RangeFFT'][3])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 2:
            self.plotter.fft_1d_plot(frame_id, loop_id, chirp_id, lane_id, 1)

            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[1])
            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['RangeFFT'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['RangeFFT'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['RangeFFT'][4])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 3:
            self.plotter.fft_2d_plot(frame_id, loop_id, lane_id, False)

            self.window.result_frame.mplc_2d.axes.imshow(
                self.plotter.plot_result[0],
                extent=[
                    self.plotter.plot_result[1],
                    self.plotter.plot_result[2],
                    self.plotter.plot_result[3],
                    self.plotter.plot_result[4]
                ],
                aspect='auto'
            )
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['DopplerFFT'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['DopplerFFT'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['DopplerFFT'][2])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 4:
            self.plotter.time_domain_plot(frame_id, loop_id, chirp_id, lane_id)

            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[1])
            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[2])
            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['TimeDomain'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['TimeDomain'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['TimeDomain'][2])
            self.window.result_frame.mplc_2d.figure.legend([
                self.strings['PlotLegend']['TimeDomain'][3],
                self.strings['PlotLegend']['TimeDomain'][4]
            ])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 5:

            guard_cell = self.window.result_frame.guard_cell_sb.value()
            training_cell = self.window.result_frame.training_cell_sb.value()

            self.plotter.ca_cfar_plot(frame_id, loop_id, chirp_id, lane_id, guard_cell, training_cell)

            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[1])
            self.window.result_frame.mplc_2d.axes.plot(self.plotter.plot_result[0], self.plotter.plot_result[2])
            for elem in self.plotter.plot_result[3]:
                self.window.result_frame.mplc_2d.axes.plot(elem[0], elem[1], 'X')

            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['CFAR'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['CFAR'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['CFAR'][2])
            self.window.result_frame.mplc_2d.figure.legend([
                self.strings['PlotLegend']['CFAR'][3],
                self.strings['PlotLegend']['CFAR'][4]
            ])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 6:

            self.plotter.fft_2d_plot(frame_id, loop_id, lane_id, True)

            self.window.result_frame.mplc_3d.axes.clear()

            self.window.result_frame.mplc_3d.axes.plot_surface(
                self.plotter.plot_result[0],
                self.plotter.plot_result[1],
                self.plotter.plot_result[2],
                cmap='rainbow'
            )

            self.window.result_frame.mplc_3d.axes.set_xlabel(self.strings['PlotLegend']['DopplerFFT'][0])
            self.window.result_frame.mplc_3d.axes.set_ylabel(self.strings['PlotLegend']['DopplerFFT'][1])
            self.window.result_frame.mplc_3d.axes.set_zlabel(self.strings['PlotLegend']['DopplerFFT'][3])
            self.window.result_frame.mplc_3d.figure.suptitle(self.strings['PlotLegend']['DopplerFFT'][4])
            self.window.result_frame.mplc_3d.draw()

            self.window.result_frame.mplc_2d.hide()
            self.window.result_frame.mplc_3d.show()

        elif plot_type == 7:
            self.plotter.angle_of_arrival_plot(frame_id, loop_id)

            self.window.result_frame.mplc_2d.axes.imshow(
                self.plotter.plot_result[0],
                extent=[
                    self.plotter.plot_result[1],
                    self.plotter.plot_result[2],
                    self.plotter.plot_result[3],
                    self.plotter.plot_result[4]
                ],
                aspect='auto'
            )

            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['AngleFFT'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['AngleFFT'][1])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['AngleFFT'][2])
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

        elif plot_type == 8:
            guard_cell = self.window.result_frame.guard_cell_sb.value()
            training_cell = self.window.result_frame.training_cell_sb.value()

            self.plotter.detected_obj_plot(frame_id, loop_id, chirp_id, lane_id, guard_cell, training_cell)

            legend = ["device"]
            self.window.result_frame.mplc_2d.axes.plot(0, 0, '*', markersize=11)
            for i in range(len(self.plotter.plot_result[1])):
                self.window.result_frame.mplc_2d.axes.plot(
                    self.plotter.plot_result[1][i][0],
                    self.plotter.plot_result[1][i][1],
                    'o'
                )
                legend.append(f"obj {i+1}")

            self.window.result_frame.mplc_2d.axes.grid()
            self.window.result_frame.mplc_2d.figure.supxlabel(self.strings['PlotLegend']['DetectedObj'][0])
            self.window.result_frame.mplc_2d.figure.supylabel(self.strings['PlotLegend']['DetectedObj'][0])
            self.window.result_frame.mplc_2d.figure.suptitle(self.strings['PlotLegend']['DetectedObj'][1])
            self.window.result_frame.mplc_2d.figure.legend(legend)
            self.window.result_frame.mplc_2d.draw()

            self.window.result_frame.mplc_2d.show()
            self.window.result_frame.mplc_3d.hide()

    @staticmethod
    def network_settings():
        os.system('control.exe ncpa.cpl')

    @staticmethod
    def exit():
        sys.exit()
