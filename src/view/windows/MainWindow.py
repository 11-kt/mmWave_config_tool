import importlib.resources
import yaml

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from view.frames.StartFrame import StartFrame
from view.frames.SignalConfigurationFrame import SignalConfigurationFrame
from view.frames.WaitFrame import WaitFrame
from view.frames.ResultFrame import ResultFrame


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Title
        self.setWindowTitle('mmWave_config_tool')

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Window Size
        self.setMinimumSize(900, 900)

        # String resources
        with importlib.resources.path("resources.strings", 'strings.yaml') as path:
            with open(path) as f:
                self.strings = yaml.safe_load(f)
        with importlib.resources.path("resources.raw_data", "adc_data_Raw_0.bin") as path:
            self.default_working_directory = str(path).replace("\\adc_data_Raw_0.bin", "")
        with importlib.resources.path("resources.drawable", 'chirp_example.png') as path:
            self.chirp_example_img = str(path)
        with importlib.resources.path("resources.drawable", "success.png") as path:
            self.successfully_image = str(path)
        with importlib.resources.path("resources.drawable", "wait.gif") as path:
            self.gif = str(path)
        with importlib.resources.path("resources.drawable", "error.png") as path:
            self.error_image = str(path)

        # Frames
        self.start_frame = StartFrame(self.strings)
        self.signal_conf_frame = SignalConfigurationFrame(
            self.strings,
            self.default_working_directory,
            self.chirp_example_img
        )
        self.wait_frame = WaitFrame(
            self.strings,
            self.successfully_image,
            self.gif,
            self.error_image
        )
        self.result_frame = ResultFrame(self.strings)

    def rebuild_wait_frame(self):
        self.wait_frame = WaitFrame(
            self.strings,
            self.successfully_image,
            self.gif,
            self.error_image
        )

    def rebuild_result_frame(self):
        self.result_frame = ResultFrame(self.strings)
