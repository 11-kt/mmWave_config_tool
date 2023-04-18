from PyQt6.QtWidgets import QWidget, QVBoxLayout
from view.frames.StartFrame import StartFrame
from view.frames.SignalConfigurationFrame import SignalConfigurationFrame


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Title
        self.setWindowTitle('mmWave_config_tool')

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Window Size
        self.setMinimumSize(800, 800)

        # Frames
        self.start_frame = StartFrame()
        self.signal_conf_frame = SignalConfigurationFrame()
