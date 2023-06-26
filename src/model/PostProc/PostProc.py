import numpy as np
import csv
import importlib.resources
import gc

from model.PostProc.TimeDomain import real_image_plot
from model.PostProc.FFT_1D import fft_1d
from model.PostProc.FFT_2D import fft_2d
from model.PostProc.CA_CFAR_1D import ca_cfar_1d
from model.PostProc.FFT_3D import angle_of_arrival_2d
from model.PostProc.ObjectDetection import detected_object


class PostProc:

    def __init__(self, profile_dict: dict, chirp_dict: dict, tx_ena: int, rx_ena: int, adc_bits: int, path: str,
                 data_type: bool, num_frames: int, num_loops: int, num_chirps: int):

        self.profiles: dict = profile_dict

        self.chirps: dict = chirp_dict

        self.tx: int = tx_ena

        self.rx: int = rx_ena

        self.num_ADC_bits: int = adc_bits

        self.file_path: str = path

        self.num_lanes: int = 4

        # Тип обрабатываемых данных
        # False = complex, True = real
        self.data_type: bool = data_type

        self.num_frames: int = num_frames

        self.num_loops: int = num_loops

        self.num_chirps: int = num_chirps

        if 0 in self.profiles.keys():
            self.adc_sample_rate: int = self.profiles[0].adc_sample_rate

        elif 1 in self.profiles.keys():
            self.adc_sample_rate: int = self.profiles[1].adc_sample_rate

        elif 2 in self.profiles.keys():
            self.adc_sample_rate: int = self.profiles[2].adc_sample_rate

        else:
            self.adc_sample_rate: int = self.profiles[3].adc_sample_rate

        # Массив данных, сгруппированных по полосам
        self.reshaped_adc_data = None

        # Массив данных, сгруппированный для удобного построения графиков
        self.plot_data: list = []

        # Массив данных, которые подготовлены для отрисовки
        self.plot_result = None

    def read_binary_file(self):
        with open(self.file_path, 'r') as f:

            adc_data = np.fromfile(f, np.int16)

            if self.num_ADC_bits != 16:
                l_max = 2 ** (self.num_ADC_bits - 1) - 1

                for i in range(len(adc_data)):
                    if adc_data[i] > l_max:
                        adc_data[i] = adc_data[i] - 2 ** self.num_ADC_bits
            f.close()

        return adc_data

    def organize_data_by_lane(self):
        adc_data = self.read_binary_file()

        self.reshaped_adc_data = []
        if self.data_type:
            self.reshaped_adc_data = np.reshape(a=adc_data, newshape=(-1, self.num_lanes))

        else:
            adc_data = np.reshape(a=adc_data, newshape=(-1, self.num_lanes * 2))

            for j in range(len(adc_data)):
                self.reshaped_adc_data.append([
                    adc_data[j][0] + 1j * adc_data[j][4],
                    adc_data[j][1] + 1j * adc_data[j][5],
                    adc_data[j][2] + 1j * adc_data[j][6],
                    adc_data[j][3] + 1j * adc_data[j][7],
                ])

        del adc_data
        gc.collect()
        return True

    def write_csv_data(self):
        if self.reshaped_adc_data is not None:
            with importlib.resources.path("resources.raw_data", 'result.csv') as path:
                with open(path, 'w', newline='') as csv_file:
                    writer = csv.DictWriter(
                        f=csv_file,
                        fieldnames=['First Line', 'Second Line', 'Third Line', 'Fourth Line']
                    )
                    writer.writeheader()

                    for j in range(len(self.reshaped_adc_data)):
                        writer.writerow(
                            {
                                'First Line': self.reshaped_adc_data[j][0], 'Second Line': self.reshaped_adc_data[j][1],
                                'Third Line': self.reshaped_adc_data[j][2], 'Fourth Line': self.reshaped_adc_data[j][3]
                            }
                        )

            del self.reshaped_adc_data
            gc.collect()

    def organize_data_per_frame_loop_chirp_antenna_sample(self):
        current_elem = 0

        for _ in range(self.num_frames):

            self.plot_data.append([])

            current_frame = len(self.plot_data) - 1

            for _ in range(self.num_loops):
                self.plot_data[current_frame].append([])

                current_loop = len(self.plot_data[current_frame]) - 1

                for _ in range(self.num_chirps):

                    self.plot_data[current_frame][current_loop].append([])

                    current_chirp = len(self.plot_data[current_frame][current_loop]) - 1

                    self.plot_data[current_frame][current_loop][current_chirp].append([])
                    self.plot_data[current_frame][current_loop][current_chirp].append([])
                    self.plot_data[current_frame][current_loop][current_chirp].append([])
                    self.plot_data[current_frame][current_loop][current_chirp].append([])

                    for _ in range(self.adc_sample_rate):
                        self.plot_data[current_frame][current_loop][current_chirp][0]\
                            .append(self.reshaped_adc_data[current_elem][0])

                        self.plot_data[current_frame][current_loop][current_chirp][1]\
                            .append(self.reshaped_adc_data[current_elem][1])

                        self.plot_data[current_frame][current_loop][current_chirp][2]\
                            .append(self.reshaped_adc_data[current_elem][2])

                        self.plot_data[current_frame][current_loop][current_chirp][3]\
                            .append(self.reshaped_adc_data[current_elem][3])

                        current_elem += 1
        return True

    def fft_1d_plot(self, frame_id, loop_id, chirp_id, lane_id, type_plot):
        del self.plot_result
        gc.collect()

        freq_slope = 0
        sample_rate = 0
        for value in self.chirps.values():
            if chirp_id + 1 in range(value.chirp_start_cfg_id, value.chirp_end_cfg_id + 1):
                freq_slope = self.profiles[value.profile_id].freq_slope + value.freq_slope_var
                sample_rate = self.profiles[value.profile_id].sample_rate

        self.plot_result = fft_1d(
            chirp=self.plot_data[frame_id][loop_id][chirp_id][lane_id],
            type_plot=type_plot,
            data_type=self.data_type,
            freq_slope=freq_slope,
            sample_rate=sample_rate,
            adc_sample_rate=self.adc_sample_rate
        )

    def fft_2d_plot(self, frame_id, loop_id, lane_id, is_3d):
        del self.plot_result
        gc.collect()

        frame = []
        for i in range(self.num_chirps):
            frame.append(self.plot_data[frame_id][loop_id][i][lane_id])

        last_profile = self.profiles.popitem()
        idle_time = last_profile[1].idle_time
        ramp_time = last_profile[1].ramp_end_time
        freq_slope = last_profile[1].freq_slope
        start_freq = last_profile[1].start_freq
        sample_rate = last_profile[1].sample_rate
        self.profiles[last_profile[0]] = last_profile[1]
        self.plot_result = fft_2d(
            tx=self.tx,
            frame=frame,
            data_type=self.data_type,
            idle_time=idle_time,
            ramp_time=ramp_time,
            chirp_num=self.num_chirps,
            freq_slope=freq_slope,
            start_freq=start_freq,
            sample_rate=sample_rate,
            adc_sample_rate=self.adc_sample_rate,
            is_3d=is_3d
        )

    def time_domain_plot(self, frame_id, loop_id, chirp_id, lane_id):
        del self.plot_result
        gc.collect()

        self.plot_result = real_image_plot(self.plot_data[frame_id][loop_id][chirp_id][lane_id])

    def ca_cfar_plot(self, frame_id, loop_id, chirp_id, lane_id, guard_cell, training_cell):
        del self.plot_result
        gc.collect()

        p_fa = 10 ** -guard_cell
        freq_slope = 0
        sample_rate = 0

        for value in self.chirps.values():
            if chirp_id + 1 in range(value.chirp_start_cfg_id, value.chirp_end_cfg_id + 1):
                freq_slope = self.profiles[value.profile_id].freq_slope + value.freq_slope_var
                sample_rate = self.profiles[value.profile_id].sample_rate

        self.plot_result = ca_cfar_1d(
            chirp=self.plot_data[frame_id][loop_id][chirp_id][lane_id],
            guard_cell=guard_cell,
            training_cell=training_cell,
            p_fa=p_fa,
            adc_sample_rate=self.adc_sample_rate,
            freq_slope=freq_slope,
            sample_rate=sample_rate,
            data_type=self.data_type
        )

    def angle_of_arrival_plot(self, frame_id, loop_id):
        del self.plot_result
        gc.collect()

        last_profile = self.profiles.popitem()
        freq_slope = last_profile[1].freq_slope
        adc_sample_rate = last_profile[1].adc_sample_rate
        sample_rate = last_profile[1].sample_rate
        self.profiles[last_profile[0]] = last_profile[1]

        self.plot_result = angle_of_arrival_2d(
            tx=self.tx,
            rx=self.rx,
            frame=self.plot_data[frame_id][loop_id],
            freq_slope=freq_slope,
            sample_rate=sample_rate,
            adc_sample_rate=adc_sample_rate,
            data_type=self.data_type
        )

    def detected_obj_plot(self, frame_id, loop_id, chirp_id, lane_id, guard_cell, training_cell):
        del self.plot_result
        gc.collect()

        p_fa = 10 ** -guard_cell
        freq_slope = 0
        sample_rate = 0
        for value in self.chirps.values():
            if chirp_id + 1 in range(value.chirp_start_cfg_id, value.chirp_end_cfg_id + 1):
                freq_slope = self.profiles[value.profile_id].freq_slope + value.freq_slope_var
                sample_rate = self.profiles[value.profile_id].sample_rate

        self.plot_result = detected_object(
            chirp=self.plot_data[frame_id][loop_id][chirp_id][lane_id],
            frame=self.plot_data[frame_id][loop_id],
            guard_cell=guard_cell,
            training_cell=training_cell,
            p_fa=p_fa,
            data_type=self.data_type,
            tx=self.tx,
            rx=self.rx,
            freq_slope=freq_slope,
            sample_rate=sample_rate,
            adc_sample_rate=self.adc_sample_rate
        )

    def clear_data(self):
        del self.reshaped_adc_data
        del self.plot_result
        del self.plot_data
        del self.profiles
        del self.chirps
        gc.collect()

        self.plot_data = []
