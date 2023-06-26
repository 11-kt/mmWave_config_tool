from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout, QLabel, QDoubleSpinBox, \
    QSpinBox, QComboBox, QCheckBox, QPushButton, QLineEdit, QSizePolicy


class SignalConfigurationFrame(QFrame):

    def __init__(self, strings: dict, default_working_directory: str, chirp_example_img: str):
        super(SignalConfigurationFrame, self).__init__()

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.strings = strings

        self.default_working_directory = default_working_directory

        # Sub Layout 1
        self.sub_layout_1 = QHBoxLayout()

        # Sensor Configuration GB
        self.sensor_config_gb = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][0])
        self.sub_layout_1.addWidget(self.sensor_config_gb)
        # GP Layout
        self.form_layout = QFormLayout()
        self.sensor_config_gb.setLayout(self.form_layout)
        # Profile & spinbox
        self.profile = QLabel(self.strings['SignalConfigurationFrame']['profile'][0])
        self.profile.setToolTip(self.strings['SignalConfigurationFrame']['profile'][1])
        self.profile_sb = QSpinBox()
        self.profile_sb.setMaximum(3)
        self.form_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.profile)
        self.form_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.profile_sb)
        # Start Freq & spinbox
        self.start_freq = QLabel(self.strings['SignalConfigurationFrame']['start_freq'][0])
        self.start_freq.setToolTip(self.strings['SignalConfigurationFrame']['start_freq'][1])
        self.start_freq_sb = QDoubleSpinBox()
        self.start_freq_sb.setDecimals(6)
        self.start_freq_sb.setValue(77.000000)
        self.start_freq_sb.setRange(76.000000, 81.000000)
        self.form_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.start_freq)
        self.form_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.start_freq_sb)
        # Freq slope & spinbox
        self.freq_slope = QLabel(self.strings['SignalConfigurationFrame']['freq_slope'][0])
        self.freq_slope.setToolTip(self.strings['SignalConfigurationFrame']['freq_slope'][1])
        self.freq_slope_sb = QDoubleSpinBox()
        self.freq_slope_sb.setDecimals(3)
        self.freq_slope_sb.setValue(29.982)
        self.freq_slope_sb.setRange(-100.000, 100.000)
        self.form_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.freq_slope)
        self.form_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.freq_slope_sb)
        # Idle Time & spinbox
        self.idle_time = QLabel(self.strings['SignalConfigurationFrame']['idle_time'][0])
        self.idle_time.setToolTip(self.strings['SignalConfigurationFrame']['idle_time'][1])
        self.idle_time_sb = QDoubleSpinBox()
        self.idle_time_sb.setMaximum(5242.87)
        self.idle_time_sb.setValue(100.00)
        self.form_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.idle_time)
        self.form_layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.idle_time_sb)
        # ADC Start Time & spinbox
        self.adc_st = QLabel(self.strings['SignalConfigurationFrame']['adc_st'][0])
        self.adc_st.setToolTip(self.strings['SignalConfigurationFrame']['adc_st'][1])
        self.adc_st_sb = QDoubleSpinBox()
        self.adc_st_sb.setValue(6.00)
        self.adc_st_sb.setMaximum(40.95)
        self.form_layout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.adc_st)
        self.form_layout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.adc_st_sb)
        # Ramp End Time & spinbox
        self.ramp_et = QLabel(self.strings['SignalConfigurationFrame']['ramp_et'][0])
        self.ramp_et.setToolTip(self.strings['SignalConfigurationFrame']['ramp_et'][1])
        self.ramp_et_sb = QDoubleSpinBox()
        self.ramp_et_sb.setValue(60.00)
        self.ramp_et_sb.setMaximum(5000.00)
        self.form_layout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.ramp_et)
        self.form_layout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.ramp_et_sb)
        # TX0 Out Power Backoff Code & combobox
        self.tx0_Out_Power_Backoff_Code = QLabel(self.strings['SignalConfigurationFrame']
                                                 ['tx_Out_Power_Backoff_Code'][0])
        self.tx0_Out_Power_Backoff_Code.setToolTip(self.strings['SignalConfigurationFrame']
                                                   ['tx_Out_Power_Backoff_Code'][1])
        self.tx0_Out_Power_Backoff_Code_cb = QComboBox()
        self.tx0_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][4], 0
        )
        self.tx0_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][5], 3
        )
        self.tx0_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][6], 6
        )
        self.tx0_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][7], 9
        )
        self.form_layout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.tx0_Out_Power_Backoff_Code)
        self.form_layout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.tx0_Out_Power_Backoff_Code_cb)
        # TX1 Out Power Backoff Code & combobox
        self.tx1_Out_Power_Backoff_Code = QLabel(self.strings['SignalConfigurationFrame']
                                                 ['tx_Out_Power_Backoff_Code'][2])
        self.tx1_Out_Power_Backoff_Code.setToolTip(self.strings['SignalConfigurationFrame']
                                                   ['tx_Out_Power_Backoff_Code'][1])
        self.tx1_Out_Power_Backoff_Code_cb = QComboBox()
        self.tx1_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][4], 0
        )
        self.tx1_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][5], 3
        )
        self.tx1_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][6], 6
        )
        self.tx1_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][7], 9
        )
        self.form_layout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.tx1_Out_Power_Backoff_Code)
        self.form_layout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.tx1_Out_Power_Backoff_Code_cb)
        # TX2 Out Power Backoff Code & combobox
        self.tx2_Out_Power_Backoff_Code = QLabel(self.strings['SignalConfigurationFrame']
                                                 ['tx_Out_Power_Backoff_Code'][3])
        self.tx2_Out_Power_Backoff_Code.setToolTip(self.strings['SignalConfigurationFrame']
                                                   ['tx_Out_Power_Backoff_Code'][1])
        self.tx2_Out_Power_Backoff_Code_cb = QComboBox()
        self.tx2_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][4], 0
        )
        self.tx2_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][5], 3
        )
        self.tx2_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][6], 6
        )
        self.tx2_Out_Power_Backoff_Code_cb.addItem(
            self.strings['SignalConfigurationFrame']['tx_Out_Power_Backoff_Code'][7], 9
        )
        self.form_layout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.tx2_Out_Power_Backoff_Code)
        self.form_layout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.tx2_Out_Power_Backoff_Code_cb)
        # TX0 Phase Shift & spinbox
        self.tx0_Phase_Shifter = QLabel(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][0])
        self.tx0_Phase_Shifter.setToolTip(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][1])
        self.tx0_Phase_Shifter_sb = QDoubleSpinBox()
        self.tx0_Phase_Shifter_sb.setDecimals(1)
        self.tx0_Phase_Shifter_sb.setMaximum(360)
        self.form_layout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.tx0_Phase_Shifter)
        self.form_layout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.tx0_Phase_Shifter_sb)
        # TX1 Phase Shift & spinbox
        self.tx1_Phase_Shifter = QLabel(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][2])
        self.tx1_Phase_Shifter.setToolTip(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][1])
        self.tx1_Phase_Shifter_sb = QDoubleSpinBox()
        self.tx1_Phase_Shifter_sb.setDecimals(1)
        self.tx1_Phase_Shifter_sb.setMaximum(360)
        self.form_layout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.tx1_Phase_Shifter)
        self.form_layout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.tx1_Phase_Shifter_sb)
        # TX2 Phase Shift & spinbox
        self.tx2_Phase_Shifter = QLabel(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][3])
        self.tx2_Phase_Shifter.setToolTip(self.strings['SignalConfigurationFrame']['tx_Phase_Shifter'][1])
        self.tx2_Phase_Shifter_sb = QDoubleSpinBox()
        self.tx2_Phase_Shifter_sb.setDecimals(1)
        self.tx2_Phase_Shifter_sb.setMaximum(360)
        self.form_layout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.tx2_Phase_Shifter)
        self.form_layout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.tx2_Phase_Shifter_sb)
        # TX Start Time & spinbox
        self.tx_Start_Time = QLabel(self.strings['SignalConfigurationFrame']['tx_Start_Time'][0])
        self.tx_Start_Time.setToolTip(self.strings['SignalConfigurationFrame']['tx_Start_Time'][1])
        self.tx_Start_Time_sb = QDoubleSpinBox()
        self.tx_Start_Time_sb.setRange(-40.96, 40.95)
        self.form_layout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.tx_Start_Time)
        self.form_layout.setWidget(12, QFormLayout.ItemRole.FieldRole, self.tx_Start_Time_sb)
        # Num ADC Samples & spinbox
        self.num_Adc_Samples_profile = QLabel(self.strings['SignalConfigurationFrame']['num_Adc_Samples_profile'][0])
        self.num_Adc_Samples_profile.setToolTip(self.strings['SignalConfigurationFrame']['num_Adc_Samples_profile'][1])
        self.num_Adc_Samples_profile_sb = QSpinBox()
        self.num_Adc_Samples_profile_sb.setMaximum(1024)
        self.num_Adc_Samples_profile_sb.setValue(256)
        self.form_layout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.num_Adc_Samples_profile)
        self.form_layout.setWidget(13, QFormLayout.ItemRole.FieldRole, self.num_Adc_Samples_profile_sb)
        # Dig Out Sample Rate & spinbox
        self.dig_Out_Sample_Rate = QLabel(self.strings['SignalConfigurationFrame']['dig_Out_Sample_Rate'][0])
        self.dig_Out_Sample_Rate.setToolTip(self.strings['SignalConfigurationFrame']['dig_Out_Sample_Rate'][1])
        self.dig_Out_Sample_Rate_sb = QSpinBox()
        self.dig_Out_Sample_Rate_sb.setRange(2000, 37500)
        self.dig_Out_Sample_Rate_sb.setValue(10000)
        self.form_layout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.dig_Out_Sample_Rate)
        self.form_layout.setWidget(14, QFormLayout.ItemRole.FieldRole, self.dig_Out_Sample_Rate_sb)
        # HPF 1 Corner Freq & spinbox
        self.hpf_Corner_Freq1 = QLabel(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][0])
        self.hpf_Corner_Freq1.setToolTip(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][1])
        self.hpf_Corner_Freq1_cb = QComboBox()
        self.hpf_Corner_Freq1_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][2], 0)
        self.hpf_Corner_Freq1_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][3], 1)
        self.hpf_Corner_Freq1_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][4], 2)
        self.hpf_Corner_Freq1_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq1'][5], 3)
        self.form_layout.setWidget(15, QFormLayout.ItemRole.LabelRole, self.hpf_Corner_Freq1)
        self.form_layout.setWidget(15, QFormLayout.ItemRole.FieldRole, self.hpf_Corner_Freq1_cb)
        # HPF 2 Corner Freq & spinbox
        self.hpf_Corner_Freq2 = QLabel(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][0])
        self.hpf_Corner_Freq2.setToolTip(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][1])
        self.hpf_Corner_Freq2_cb = QComboBox()
        self.hpf_Corner_Freq2_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][2], 0)
        self.hpf_Corner_Freq2_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][3], 1)
        self.hpf_Corner_Freq2_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][4], 2)
        self.hpf_Corner_Freq2_cb.addItem(self.strings['SignalConfigurationFrame']['hpf_Corner_Freq2'][5], 3)
        self.form_layout.setWidget(16, QFormLayout.ItemRole.LabelRole, self.hpf_Corner_Freq2)
        self.form_layout.setWidget(16, QFormLayout.ItemRole.FieldRole, self.hpf_Corner_Freq2_cb)
        # RX Gain & spinbox
        self.rx_Gain = QLabel(self.strings['SignalConfigurationFrame']['rx_Gain'][0])
        self.rx_Gain.setToolTip(self.strings['SignalConfigurationFrame']['rx_Gain'][1])
        self.rx_Gain_cb = QComboBox()
        for i in range(24, 54, 2):
            self.rx_Gain_cb.addItem(str(i), i)

        self.form_layout.setWidget(17, QFormLayout.ItemRole.LabelRole, self.rx_Gain)
        self.form_layout.setWidget(17, QFormLayout.ItemRole.FieldRole, self.rx_Gain_cb)

        # Bandwidth calc
        self.bandwidth_label = QLabel(self.strings['SignalConfigurationFrame']['bandwidth'][0])
        # Bandwidth val
        self.bandwidth_val_label = QLabel(self.strings['SignalConfigurationFrame']['bandwidth'][1])
        self.form_layout.setWidget(18, QFormLayout.ItemRole.LabelRole, self.bandwidth_label)
        self.form_layout.setWidget(18, QFormLayout.ItemRole.FieldRole, self.bandwidth_val_label)

        # Range resolution
        self.range_resolution_label = QLabel(self.strings['SignalConfigurationFrame']['range_resolution'][0])
        # Range resolution val
        self.range_resolution_val_label = QLabel(self.strings['SignalConfigurationFrame']['range_resolution'][1])
        self.form_layout.setWidget(19, QFormLayout.ItemRole.LabelRole, self.range_resolution_label)
        self.form_layout.setWidget(19, QFormLayout.ItemRole.FieldRole, self.range_resolution_val_label)

        # Set profile
        self.set_profile_label = QLabel(self.strings['SignalConfigurationFrame']['profile_Set'][0])
        self.set_profile_button = QPushButton(self.strings['SignalConfigurationFrame']['profile_Set'][1])
        self.form_layout.setWidget(20, QFormLayout.ItemRole.LabelRole, self.set_profile_label)
        self.form_layout.setWidget(20, QFormLayout.ItemRole.FieldRole, self.set_profile_button)

        # Chirp Configuration Layout
        self.chirp_config_layout = QHBoxLayout()
        # Chirp example Layout
        self.chirp_example_layout = QVBoxLayout()
        self.chirp_example_layout.addLayout(self.chirp_config_layout)
        self.sub_layout_1.addLayout(self.chirp_example_layout)

        # Chirp Configuration GB
        self.chirp_config_gb = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][1])
        self.chirp_config_layout.addWidget(self.chirp_config_gb)
        # GP Layout
        self.form_layout_chirp = QFormLayout()
        self.chirp_config_gb.setLayout(self.form_layout_chirp)
        # Profile id & spinbox
        self.profile_Id = QLabel(self.strings['SignalConfigurationFrame']['profile_Id'][0])
        self.profile_Id.setToolTip(self.strings['SignalConfigurationFrame']['profile_Id'][1])
        self.profile_Id_cb = QComboBox()
        self.profile_Id_cb.addItem(self.strings['SignalConfigurationFrame']['profile_Id'][3], 0)
        self.profile_Id_cb.model().item(0).setEnabled(False)
        self.profile_Id_cb.addItem(self.strings['SignalConfigurationFrame']['profile_Id'][4], 1)
        self.profile_Id_cb.model().item(1).setEnabled(False)
        self.profile_Id_cb.addItem(self.strings['SignalConfigurationFrame']['profile_Id'][5], 2)
        self.profile_Id_cb.model().item(2).setEnabled(False)
        self.profile_Id_cb.addItem(self.strings['SignalConfigurationFrame']['profile_Id'][6], 3)
        self.profile_Id_cb.model().item(3).setEnabled(False)
        self.form_layout_chirp.setWidget(0, QFormLayout.ItemRole.LabelRole, self.profile_Id)
        self.form_layout_chirp.setWidget(0, QFormLayout.ItemRole.FieldRole, self.profile_Id_cb)
        # Chirp Start id & spinbox
        self.chirp_Start_Idx = QLabel(self.strings['SignalConfigurationFrame']['chirp_Start_Idx'][0])
        self.chirp_Start_Idx.setToolTip(self.strings['SignalConfigurationFrame']['chirp_Start_Idx'][1])
        self.chirp_Start_Idx_sb = QSpinBox()
        self.chirp_Start_Idx_sb.setRange(1, 512)
        self.form_layout_chirp.setWidget(1, QFormLayout.ItemRole.LabelRole, self.chirp_Start_Idx)
        self.form_layout_chirp.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chirp_Start_Idx_sb)
        # Chirp End id & spinbox
        self.chirp_End_Idx = QLabel(self.strings['SignalConfigurationFrame']['chirp_End_Idx'][0])
        self.chirp_End_Idx.setToolTip(self.strings['SignalConfigurationFrame']['chirp_End_Idx'][1])
        self.chirp_End_Idx_sb = QSpinBox()
        self.chirp_End_Idx_sb.setRange(1, 512)
        self.chirp_End_Idx_sb.setValue(128)
        self.form_layout_chirp.setWidget(2, QFormLayout.ItemRole.LabelRole, self.chirp_End_Idx)
        self.form_layout_chirp.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chirp_End_Idx_sb)
        # Start Freq Var & spinbox
        self.start_Freq_Var = QLabel(self.strings['SignalConfigurationFrame']['start_Freq_Var'][0])
        self.start_Freq_Var.setToolTip(self.strings['SignalConfigurationFrame']['start_Freq_Var'][1])
        self.start_Freq_Var_sb = QDoubleSpinBox()
        self.start_Freq_Var_sb.setMaximum(453.000000)
        self.start_Freq_Var_sb.setDecimals(6)
        self.form_layout_chirp.setWidget(3, QFormLayout.ItemRole.LabelRole, self.start_Freq_Var)
        self.form_layout_chirp.setWidget(3, QFormLayout.ItemRole.FieldRole, self.start_Freq_Var_sb)
        # Freq Slope Var & spinbox
        self.freq_Slope_Var = QLabel(self.strings['SignalConfigurationFrame']['freq_Slope_Var'][0])
        self.freq_Slope_Var.setToolTip(self.strings['SignalConfigurationFrame']['freq_Slope_Var'][1])
        self.freq_Slope_Var_sb = QDoubleSpinBox()
        self.freq_Slope_Var_sb.setMaximum(302.400)
        self.freq_Slope_Var_sb.setDecimals(3)
        self.form_layout_chirp.setWidget(4, QFormLayout.ItemRole.LabelRole, self.freq_Slope_Var)
        self.form_layout_chirp.setWidget(4, QFormLayout.ItemRole.FieldRole, self.freq_Slope_Var_sb)
        # Idle Time Var & spinbox
        self.idle_Time_Var = QLabel(self.strings['SignalConfigurationFrame']['idle_Time_Var'][0])
        self.idle_Time_Var.setToolTip(self.strings['SignalConfigurationFrame']['idle_Time_Var'][1])
        self.idle_Time_Var_sb = QDoubleSpinBox()
        self.idle_Time_Var_sb.setMaximum(40.96)
        self.form_layout_chirp.setWidget(5, QFormLayout.ItemRole.LabelRole, self.idle_Time_Var)
        self.form_layout_chirp.setWidget(5, QFormLayout.ItemRole.FieldRole, self.idle_Time_Var_sb)
        # ADC Start Time Var & spinbox
        self.adc_Start_Time_Var = QLabel(self.strings['SignalConfigurationFrame']['adc_Start_Time_Var'][0])
        self.adc_Start_Time_Var.setToolTip(self.strings['SignalConfigurationFrame']['adc_Start_Time_Var'][1])
        self.adc_Start_Time_Var_sb = QDoubleSpinBox()
        self.adc_Start_Time_Var_sb.setMaximum(40.96)
        self.form_layout_chirp.setWidget(6, QFormLayout.ItemRole.LabelRole, self.adc_Start_Time_Var)
        self.form_layout_chirp.setWidget(6, QFormLayout.ItemRole.FieldRole, self.adc_Start_Time_Var_sb)
        # TX Enable & spinbox
        self.tx_Enable = QLabel(self.strings['SignalConfigurationFrame']['tx_Enable'][0])
        self.tx_Enable.setToolTip(self.strings['SignalConfigurationFrame']['tx_Enable'][1])
        self.tx_Enable_h_layout = QHBoxLayout()
        # Tx0
        self.tx0_en = QLabel(self.strings['SignalConfigurationFrame']['tx_Enable'][2])
        self.tx0_en_cb = QCheckBox()
        self.tx0_en_cb.setChecked(True)
        self.tx0_en_form = QFormLayout()
        self.tx0_en_form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.tx0_en)
        self.tx0_en_form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.tx0_en_cb)
        self.tx_Enable_h_layout.addLayout(self.tx0_en_form)
        # Tx1
        self.tx1_en = QLabel(self.strings['SignalConfigurationFrame']['tx_Enable'][3])
        self.tx1_en_cb = QCheckBox()
        self.tx1_en_cb.setChecked(True)
        self.tx1_en_form = QFormLayout()
        self.tx1_en_form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.tx1_en)
        self.tx1_en_form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.tx1_en_cb)
        self.tx_Enable_h_layout.addLayout(self.tx1_en_form)
        # Tx2
        self.tx2_en = QLabel(self.strings['SignalConfigurationFrame']['tx_Enable'][4])
        self.tx2_en_cb = QCheckBox()
        self.tx2_en_cb.setEnabled(False)
        self.tx2_en_form = QFormLayout()
        self.tx2_en_form.setWidget(2, QFormLayout.ItemRole.LabelRole, self.tx2_en)
        self.tx2_en_form.setWidget(2, QFormLayout.ItemRole.FieldRole, self.tx2_en_cb)
        self.tx_Enable_h_layout.addLayout(self.tx2_en_form)
        self.form_layout_chirp.setWidget(7, QFormLayout.ItemRole.LabelRole, self.tx_Enable)
        self.form_layout_chirp.setLayout(7, QFormLayout.ItemRole.FieldRole, self.tx_Enable_h_layout)
        # Step config
        self.step_layout = QHBoxLayout()
        self.set_step_label = QLabel(self.strings['SignalConfigurationFrame']['step_Set'][0])
        self.set_step_label.setToolTip(self.strings['SignalConfigurationFrame']['step_Set'][1])
        self.set_step_sb = QSpinBox()
        self.set_step_sb.setRange(0, 10)
        self.set_step_sb.setDisabled(True)
        self.step_layout.addWidget(self.set_step_label)
        self.step_layout.addWidget(self.set_step_sb)
        # Last idx config
        self.last_idx_layout = QHBoxLayout()
        self.set_idx_label = QLabel(self.strings['SignalConfigurationFrame']['step_Set'][2])
        self.set_idx_sb = QSpinBox()
        self.set_idx_sb.setRange(1, 512)
        self.set_idx_sb.setDisabled(True)
        self.set_idx_sb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        self.last_idx_layout.addWidget(self.set_idx_label)
        self.last_idx_layout.addWidget(self.set_idx_sb)
        self.form_layout_chirp.setLayout(8, QFormLayout.ItemRole.LabelRole, self.step_layout)
        self.form_layout_chirp.setLayout(8, QFormLayout.ItemRole.FieldRole, self.last_idx_layout)
        # Set chirp
        self.set_chirp_label = QLabel(self.strings['SignalConfigurationFrame']['chirp_Set'][0])
        self.set_chirp_button = QPushButton(self.strings['SignalConfigurationFrame']['chirp_Set'][1])
        self.set_chirp_button.setEnabled(False)
        self.form_layout_chirp.setWidget(9, QFormLayout.ItemRole.LabelRole, self.set_chirp_label)
        self.form_layout_chirp.setWidget(9, QFormLayout.ItemRole.FieldRole, self.set_chirp_button)

        # Frame Configuration GB
        self.frame_config_gb = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][2])
        self.chirp_config_layout.addWidget(self.frame_config_gb)
        # GP Layout
        self.form_layout_frame = QFormLayout()
        self.frame_config_gb.setLayout(self.form_layout_frame)
        # Chirp Start id & spinbox
        self.chirp_Start_Id = QLabel(self.strings['SignalConfigurationFrame']['chirp_Start_Id'][0])
        self.chirp_Start_Id.setToolTip(self.strings['SignalConfigurationFrame']['chirp_Start_Id'][1])
        self.chirp_Start_Id_sb = QSpinBox()
        self.chirp_Start_Id_sb.setRange(1, 512)
        self.chirp_Start_Id_sb.setValue(1)
        self.form_layout_frame.setWidget(0, QFormLayout.ItemRole.LabelRole, self.chirp_Start_Id)
        self.form_layout_frame.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chirp_Start_Id_sb)
        # Chirp End id & spinbox
        self.chirp_End_Id = QLabel(self.strings['SignalConfigurationFrame']['chirp_End_Id'][0])
        self.chirp_End_Id.setToolTip(self.strings['SignalConfigurationFrame']['chirp_End_Id'][1])
        self.chirp_End_Id_sb = QSpinBox()
        self.chirp_End_Id_sb.setRange(1, 512)
        self.chirp_End_Id_sb.setValue(128)
        self.form_layout_frame.setWidget(1, QFormLayout.ItemRole.LabelRole, self.chirp_End_Id)
        self.form_layout_frame.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chirp_End_Id_sb)
        # Frame Count & spinbox
        self.frame_Count = QLabel(self.strings['SignalConfigurationFrame']['frame_Count'][0])
        self.frame_Count.setToolTip(self.strings['SignalConfigurationFrame']['frame_Count'][1])
        self.frame_Count_sb = QSpinBox()
        self.frame_Count_sb.setRange(1, 65535)
        self.form_layout_frame.setWidget(2, QFormLayout.ItemRole.LabelRole, self.frame_Count)
        self.form_layout_frame.setWidget(2, QFormLayout.ItemRole.FieldRole, self.frame_Count_sb)
        # Loop Count & spinbox
        self.loop_Count = QLabel(self.strings['SignalConfigurationFrame']['loop_Count'][0])
        self.loop_Count.setToolTip(self.strings['SignalConfigurationFrame']['loop_Count'][1])
        self.loop_Count_sb = QSpinBox()
        self.loop_Count_sb.setRange(1, 255)
        self.form_layout_frame.setWidget(3, QFormLayout.ItemRole.LabelRole, self.loop_Count)
        self.form_layout_frame.setWidget(3, QFormLayout.ItemRole.FieldRole, self.loop_Count_sb)
        # Periodicity & spinbox
        self.periodicity = QLabel(self.strings['SignalConfigurationFrame']['periodicity'][0])
        self.periodicity.setToolTip(self.strings['SignalConfigurationFrame']['periodicity'][1])
        self.periodicity_sb = QDoubleSpinBox()
        self.periodicity_sb.setDecimals(7)
        self.periodicity_sb.setValue(40.0000000)
        self.periodicity_sb.setRange(0.0000003, 1342.0000000)
        self.form_layout_frame.setWidget(4, QFormLayout.ItemRole.LabelRole, self.periodicity)
        self.form_layout_frame.setWidget(4, QFormLayout.ItemRole.FieldRole, self.periodicity_sb)
        # Trigger Delay & spinbox
        self.trigger_Delay = QLabel(self.strings['SignalConfigurationFrame']['trigger_Delay'][0])
        self.trigger_Delay.setToolTip(self.strings['SignalConfigurationFrame']['trigger_Delay'][1])
        self.trigger_Delay_sb = QDoubleSpinBox()
        self.trigger_Delay_sb.setDecimals(3)
        self.trigger_Delay_sb.setMaximum(1000.000)
        self.form_layout_frame.setWidget(5, QFormLayout.ItemRole.LabelRole, self.trigger_Delay)
        self.form_layout_frame.setWidget(5, QFormLayout.ItemRole.FieldRole, self.trigger_Delay_sb)
        # Num ADC Samples & spinbox
        self.num_Adc_Samples_frame = QLabel(self.strings['SignalConfigurationFrame']['num_Adc_Samples_frame'][0])
        self.num_Adc_Samples_frame.setToolTip(self.strings['SignalConfigurationFrame']['num_Adc_Samples_frame'][1])
        self.num_Adc_Samples_frame_sb = QSpinBox()
        self.num_Adc_Samples_frame_sb.setMaximum(65535)
        self.num_Adc_Samples_frame_sb.setValue(512)
        self.num_Adc_Samples_frame_sb.setEnabled(False)
        self.form_layout_frame.setWidget(6, QFormLayout.ItemRole.LabelRole, self.num_Adc_Samples_frame)
        self.form_layout_frame.setWidget(6, QFormLayout.ItemRole.FieldRole, self.num_Adc_Samples_frame_sb)
        # Trigger Select & spinbox
        self.trigger_Select = QLabel(self.strings['SignalConfigurationFrame']['trigger_Select'][0])
        self.trigger_Select.setToolTip(self.strings['SignalConfigurationFrame']['trigger_Select'][1])
        self.trigger_Select_cb = QComboBox()
        self.trigger_Select_cb.addItem(self.strings['SignalConfigurationFrame']['trigger_Select'][2], 1)
        self.trigger_Select_cb.addItem(self.strings['SignalConfigurationFrame']['trigger_Select'][3], 2)
        self.trigger_Select_cb.model().item(1).setEnabled(False)
        self.form_layout_frame.setWidget(7, QFormLayout.ItemRole.LabelRole, self.trigger_Select)
        self.form_layout_frame.setWidget(7, QFormLayout.ItemRole.FieldRole, self.trigger_Select_cb)

        # Add example image
        # Example gp
        self.chirp_example_gp = QGroupBox('Chirp Example Image')
        # Layout
        self.chirp_example_gp_layout = QVBoxLayout()
        # Image
        self.chirp_example_img = QLabel('Chirp Example')
        self.chirp_example_img.setScaledContents(True)
        self.pixmap = QPixmap(chirp_example_img)
        self.chirp_example_img.setPixmap(self.pixmap)
        self.chirp_example_gp_layout.addWidget(self.chirp_example_img)
        self.chirp_example_gp.setLayout(self.chirp_example_gp_layout)
        self.chirp_example_layout.addWidget(self.chirp_example_gp)

        # Sub Layout 2
        self.sub_layout_2 = QVBoxLayout()
        self.sub_layout_2.addLayout(self.sub_layout_1)

        # Проверка подключения платы по CLI_CONTROL
        # Connection check gp
        self.connection_check_gp = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][3])
        self.sub_layout_2.addWidget(self.connection_check_gp)
        self.connection_check_layout = QHBoxLayout()
        # Status label
        # Neutral status
        self.neutral_connection_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][1])
        self.neutral_connection_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.neutral_connection_status.setStyleSheet("background-color: lightblue")
        self.neutral_connection_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.connection_check_layout.addWidget(self.neutral_connection_status)
        # Successful status
        self.successful_connection_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][2])
        self.successful_connection_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.successful_connection_status.setStyleSheet("background-color: lightgreen")
        self.successful_connection_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.successful_connection_status.hide()
        self.connection_check_layout.addWidget(self.successful_connection_status)
        # Unsuccessful status
        self.unsuccessful_connection_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][3])
        self.unsuccessful_connection_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unsuccessful_connection_status.setStyleSheet("background-color: red")
        self.unsuccessful_connection_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.unsuccessful_connection_status.hide()
        self.connection_check_layout.addWidget(self.unsuccessful_connection_status)
        # Connection check button
        self.connection_check_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][0])
        self.connection_check_layout.addWidget(self.connection_check_button)
        self.connection_check_gp.setLayout(self.connection_check_layout)

        # Config FPGA path gp
        self.config_fpga_path_gp = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][4])
        self.sub_layout_2.addWidget(self.config_fpga_path_gp)
        self.config_fpga_path_layout = QHBoxLayout()
        # Status label
        self.config_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][4])
        self.config_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.config_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.config_status.setStyleSheet("background-color: lightblue")
        self.config_fpga_path_layout.addWidget(self.config_status)
        # Successful status
        self.successful_config_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][5])
        self.successful_config_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.successful_config_status.setStyleSheet("background-color: lightgreen")
        self.successful_config_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.successful_config_status.hide()
        self.config_fpga_path_layout.addWidget(self.successful_config_status)
        # Unsuccessful status
        self.unsuccessful_config_status = QLabel(self.strings['SignalConfigurationFrame']['navigation'][6])
        self.unsuccessful_config_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unsuccessful_config_status.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.unsuccessful_config_status.setStyleSheet("background-color: red")
        self.unsuccessful_config_status.hide()
        self.config_fpga_path_layout.addWidget(self.unsuccessful_config_status)
        # Connection check button
        self.config_fpga_path_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][7])
        self.config_fpga_path_button.setDisabled(True)
        self.config_fpga_path_layout.addWidget(self.config_fpga_path_button)
        self.config_fpga_path_gp.setLayout(self.config_fpga_path_layout)

        # Browse result path gp
        self.browser_result_path_gp = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][5])
        self.sub_layout_2.addWidget(self.browser_result_path_gp)
        self.browser_result_path_layout = QHBoxLayout()
        # FileBrowser line
        self.result_path_browser = QLineEdit(self.default_working_directory)
        self.browser_result_path_layout.addWidget(self.result_path_browser)
        self.browser_result_path_gp.setLayout(self.browser_result_path_layout)
        # Browse button
        self.browse_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][8])
        self.browser_result_path_layout.addWidget(self.browse_button)

        # Sub Layout 3
        self.sub_layout_3 = QVBoxLayout()

        # Navigation gp
        self.navigation_gp = QGroupBox(self.strings['SignalConfigurationFrame']['GroupBoxes'][6])
        self.navigation_gp.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.navigation_gp.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.sub_layout_3.addWidget(self.navigation_gp)
        self.navigation_layout = QHBoxLayout()
        # Next button
        self.next_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][9])
        self.next_button.setDisabled(True)
        self.navigation_layout.addWidget(self.next_button)
        self.navigation_gp.setLayout(self.navigation_layout)
        # Back button
        self.back_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][10])
        self.navigation_layout.addWidget(self.back_button)
        # Exit button
        self.exit_button = QPushButton(self.strings['SignalConfigurationFrame']['navigation'][11])
        self.navigation_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(self.sub_layout_2)
        self.main_layout.addLayout(self.sub_layout_3)
