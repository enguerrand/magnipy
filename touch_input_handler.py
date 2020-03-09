import json
import re
import selectors
from json import JSONDecodeError

import evdev
from threading import Thread
from selectors import DefaultSelector, EVENT_READ

from evdev import ecodes

from pan_zoom_state import PanZoomState



class TouchInputHandler:
    def __init__(self, pan_zoom_state):
        self.pan_zoom_state = pan_zoom_state
        self.fingers_down = 0
        self.drag_start_x = None
        self.drag_start_y = None
        self.grabbed_devices = []
        self.stop_requested = False

    def listen(self):
        selector = selectors.DefaultSelector()
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        device_info = dict()
        for device in devices:
            if is_mouse(device):
                print(device.path, device.name, device.phys)
                capabilities = device.capabilities(verbose=False)
                abs_info_abs_x = extract_absinfo(capabilities, ecodes.ABS_X)
                abs_info_abs_y = extract_absinfo(capabilities, ecodes.ABS_Y)
                if abs_info_abs_x is None or abs_info_abs_y is None:
                    print("No abs_info found on x or y for device " + device.name)
                    continue
                device_info[device.path] = (abs_info_abs_x, abs_info_abs_y)
                selector.register(device, selectors.EVENT_READ)
                device.grab()
                self.grabbed_devices.append(device)

        while not self.stop_requested:
            for key, mask in selector.select(1):
                device = key.fileobj
                (abs_info_x, abs_info_abs_y) = device_info[device.path]
                x_size = abs_info_abs_x.max - abs_info_abs_x.min
                y_size = abs_info_abs_y.max - abs_info_abs_y.min
                for event in device.read():
                    if event.type == ecodes.EV_ABS:
                        if event.code == ecodes.ABS_X:
                            if self.drag_start_x is not None:
                                self.pan_zoom_state.pan_relative(delta_x=(event.value - self.drag_start_x) / x_size)
                            self.drag_start_x = event.value
                        if event.code == ecodes.ABS_Y:
                            if self.drag_start_y is not None:
                                self.pan_zoom_state.pan_relative(delta_y=(event.value - self.drag_start_y) / y_size)
                            self.drag_start_y = event.value
                        if event.code == ecodes.ABS_MT_TRACKING_ID:
                            if event.value == -1:
                                self.fingers_down = max(0, self.fingers_down - 1)
                            else:
                                self.fingers_down = self.fingers_down + 1
                            print("fingers down: " + str(self.fingers_down))
                            if self.fingers_down == 0:
                                self.drag_start_x = None
                                self.drag_start_y = None

    def stop(self):
        for dev in self.grabbed_devices:
            dev.ungrab()
        self.stop_requested = True


def extract_absinfo(capabilities, type):
    abs_info_entries = capabilities[ecodes.EV_ABS]
    for abs_info_entry in abs_info_entries:
        if abs_info_entry[0] == type:
            return abs_info_entry[1]
    return None


def is_mouse(device):
    # return re.match('.*(mouse|touchpad).*', device.name.lower())
    return re.match('.*(touchpad).*', device.name.lower())


if __name__ == '__main__':
    handler = TouchInputHandler(PanZoomState(1920, 1080, 10, 1920, 180))
    Thread(target=handler.listen, args=()).start()
