import importlib.resources
import yaml
import asyncio


from view.windows.MainWindow import MainWindow

from model.ConfigFileCreator import ConfigFileCreator
from model.ConvertingValues import ConvertingValues
from model.JsonWriter import *


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


