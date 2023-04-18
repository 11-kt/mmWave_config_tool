import os
import sys
from view.windows.MainWindow import MainWindow


class MainWindowController:

    def __init__(self):

        self.window = MainWindow()
        self.window.main_layout.addWidget(self.window.start_frame)
        self.window.show()

        # Navigation
        # Signal conf stag
        self.window.start_frame.next_button.clicked.connect(self.signal_conf_stage)
        # Network settings
        self.window.start_frame.open_nw_config.clicked.connect(self.network_settings)
        # Exit from app
        self.window.start_frame.exit_button.clicked.connect(self.exit)

    def signal_conf_stage(self):
        self.window.start_frame.hide()
        self.window.main_layout.addWidget(self.window.signal_conf_frame)

    @staticmethod
    def network_settings():
        os.system('control.exe ncpa.cpl')

    @staticmethod
    def exit():
        sys.exit(0)
