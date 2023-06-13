import json
import importlib.resources


def update_json_data_format_mode(data_format_mode: int):
    with importlib.resources.path("resources.cli_control", 'cf.json') as path:
        with open(str(path), 'r') as f:
            data = json.load(f)

        data['DCA1000Config']["dataFormatMode"] = data_format_mode

        with open(str(path), 'w') as f:
            json.dump(data, f, indent=4)


def update_json_file_path_mode(file_path: str):
    with importlib.resources.path("resources.cli_control", 'cf.json') as path:
        with open(str(path), 'r') as f:
            data = json.load(f)

        data['DCA1000Config']['captureConfig']["fileBasePath"] = file_path

        with open(str(path), 'w') as f:
            json.dump(data, f, indent=4)


def update_json_capture_config(
        num_frames: int,
        num_loops: int,
        num_chirps: int,
        num_samples: int
):
    num_bytes = num_frames * num_loops * num_chirps * num_samples * 4 * 2

    with importlib.resources.path("resources.cli_control", 'cf.json') as path:
        with open(str(path), 'r') as f:
            data = json.load(f)

        data['DCA1000Config']["captureConfig"]["bytesToCapture"] = num_bytes

        with open(str(path), 'w') as f:
            json.dump(data, f, indent=4)
