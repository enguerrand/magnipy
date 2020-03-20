import json
import os
from pathlib import Path

CONFIG_DIR = os.path.join(str(Path.home()), ".magnipy")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
RUNTIME_SETTINGS_FILE = os.path.join(CONFIG_DIR, "runtime.json")


class Config:
    def __init__(self, camera_focus_step=1, camera_fps=10, camera_res_width=3264, camera_res_height=2448):
        self.camera_focus_step = camera_focus_step
        self.camera_fps = camera_fps
        self.camera_res_width = camera_res_width
        self.camera_res_height = camera_res_height


class RuntimeSettings:
    def __init__(self, zoom=1.0, invert_colors=False, auto_focus=True, absolute_focus=35):
        self.zoom = zoom
        self.invert_colors = invert_colors
        self.auto_focus = auto_focus
        self.absolute_focus = absolute_focus


def read_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def write_json(object, path: str):
    try:
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        with open(path, "w") as f:
            json.dump(object.__dict__, f, indent=4)
    except Exception as e:
        pass


def load_config() -> Config:
    try:
        data = read_json(CONFIG_FILE)
        return Config(
            data["camera_focus_step"],
            data["camera_fps"],
            data["camera_res_width"],
            data["camera_res_height"]
        )
    except Exception as e:
        return Config()


def load_runtime_settings() -> RuntimeSettings:
    try:
        data = read_json(RUNTIME_SETTINGS_FILE)
        return RuntimeSettings(data["zoom"], data["invert_colors"], data["auto_focus"], data["absolute_focus"])
    except Exception as e:
        return RuntimeSettings()


def save_runtime_settings(settings):
    write_json(settings, RUNTIME_SETTINGS_FILE)
