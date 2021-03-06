import selectors
import evdev
from threading import Thread
from evdev import ecodes
from pan_zoom_state import PanZoomState


class DeviceState:
    def __init__(self, device, multitouch):
        self.device = device
        self.multitouch = multitouch
        self.fingers_down = 0
        self.abs_pressure = 0
        self.drag_start_x = None
        self.drag_start_y = None


class TouchInputHandler:
    def __init__(self, pan_zoom_state):
        self.pan_zoom_state = pan_zoom_state
        self.grabbed_devices = dict()
        self.stop_requested = False

    def listen(self):
        try:
            selector = selectors.DefaultSelector()
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            device_info = dict()
            for device in devices:
                capabilities = device.capabilities(verbose=False)
                mt = is_mt_touch_device(capabilities)
                if mt or is_touch_device(capabilities):
                    print(device.path, device.name, device.phys)
                    abs_info_abs_x = extract_absinfo(capabilities, ecodes.ABS_X)
                    abs_info_abs_y = extract_absinfo(capabilities, ecodes.ABS_Y)
                    if abs_info_abs_x is None or abs_info_abs_y is None:
                        print("No abs_info found on x or y for device " + device.name)
                        continue
                    device_info[device.path] = (abs_info_abs_x, abs_info_abs_y)
                    selector.register(device, selectors.EVENT_READ)
                    self.grabbed_devices[device.path] = DeviceState(device, mt)
                    device.grab()

            while not self.stop_requested:
                for ready in selector.select(1):
                    if not ready:
                        continue
                    key, mask = ready
                    device = key.fileobj
                    (abs_info_abs_x, abs_info_abs_y) = device_info[device.path]
                    x_size = abs_info_abs_x.max - abs_info_abs_x.min
                    y_size = abs_info_abs_y.max - abs_info_abs_y.min
                    for event in device.read():
                        if event.type == ecodes.EV_ABS:
                            if event.code == ecodes.ABS_X:
                                if self.grabbed_devices[device.path].drag_start_x is not None:
                                    self.pan_zoom_state.pan_relative(delta_x=(self.grabbed_devices[device.path].drag_start_x - event.value) / x_size)
                                self.grabbed_devices[device.path].drag_start_x = event.value
                            if event.code == ecodes.ABS_Y:
                                if self.grabbed_devices[device.path].drag_start_y is not None:
                                    self.pan_zoom_state.pan_relative(delta_y=(self.grabbed_devices[device.path].drag_start_y - event.value) / y_size)
                                self.grabbed_devices[device.path].drag_start_y = event.value
                            if event.code == ecodes.ABS_MT_TRACKING_ID:
                                if event.value == -1:
                                    self.grabbed_devices[device.path].fingers_down = max(0, self.grabbed_devices[device.path].fingers_down - 1)
                                else:
                                    self.grabbed_devices[device.path].fingers_down = self.grabbed_devices[device.path].fingers_down + 1
                                if self.grabbed_devices[device.path].fingers_down == 0:
                                    self.grabbed_devices[device.path].drag_start_x = None
                                    self.grabbed_devices[device.path].drag_start_y = None
                            if event.code == ecodes.ABS_PRESSURE:
                                pressure = event.value
                                self.grabbed_devices[device.path].abs_pressure = pressure
                                if not self.grabbed_devices[device.path].multitouch:
                                    if pressure <= 0:
                                        self.grabbed_devices[device.path].drag_start_x = None
                                        self.grabbed_devices[device.path].drag_start_y = None
        finally:
            for device_state in self.grabbed_devices.values():
                device_state.device.ungrab()

    def stop(self):
        self.stop_requested = True


def is_touch_device(capabilities):
    for prop in (ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_PRESSURE):
        if extract_absinfo(capabilities, prop) is None:
            return False
    return True


def is_mt_touch_device(capabilities):
    for prop in (ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_MT_TRACKING_ID):
        if extract_absinfo(capabilities, prop) is None:
            return False
    return True


def extract_absinfo(capabilities, type):
    try:
        abs_info_entries = capabilities[ecodes.EV_ABS]
        for abs_info_entry in abs_info_entries:
            if abs_info_entry[0] == type:
                return abs_info_entry[1]
        return None
    except KeyError:
        return None


if __name__ == '__main__':
    handler = TouchInputHandler(PanZoomState(1920, 1080, 10, 1920, 180))
    Thread(target=handler.listen, args=()).start()
