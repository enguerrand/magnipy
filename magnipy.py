from threading import Thread

import cv2
import sys
import persistence
from screeninfo import get_monitors

from touch_input_handler import TouchInputHandler
from pan_zoom_state import PanZoomState

config = persistence.load_config()
runtime_settings = persistence.load_runtime_settings()

KEY_CODE_BACKSPACE = 8
KEY_CODE_ENTER = 13
KEY_CODE_ESCAPE = 27
KEY_CODE_SPACE = 32
KEY_CODE_ARROW_LEFT = 65361
KEY_CODE_ARROW_UP = 65362
KEY_CODE_ARROW_RIGHT = 65363
KEY_CODE_ARROW_DOWN = 65364
DELTA = 40

video_device = "/dev/video0"
if len(sys.argv) > 1:
    video_device = "/dev/" + sys.argv[1]

cap = cv2.VideoCapture(video_device)

cap.set(cv2.CAP_PROP_FPS, config.camera_fps)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.camera_res_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.camera_res_height)
if runtime_settings.auto_focus:
    initial_auto_focus = 1
else:
    initial_auto_focus = 0
cap.set(cv2.CAP_PROP_AUTOFOCUS, initial_auto_focus)
cap.set(cv2.CAP_PROP_FOCUS, runtime_settings.absolute_focus)

touch_input_handler = None
try:
    ret, frame = cap.read()
    if frame is None:
        print("Failed to capture from device " + video_device + " => Aborting execution")
        sys.exit(-1)

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN | cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    display_width = get_monitors()[0].width
    display_height = get_monitors()[0].height
    ratio = display_width / display_height

    height, width, channels = frame.shape
    pan_zoom_state = PanZoomState(width, height, 10, display_width, display_height)
    pan_zoom_state.zoom_level = runtime_settings.zoom

    touch_input_handler = TouchInputHandler(pan_zoom_state)
    Thread(target=touch_input_handler.listen, args=()).start()

    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape

        bounds = pan_zoom_state.compute_bounds()

        cropped = frame[bounds.dy:bounds.dy + bounds.height, bounds.dx:bounds.dx + bounds.width]

        if runtime_settings.invert_colors:
            cropped = cv2.bitwise_not(cropped)

        with_borders = cv2.copyMakeBorder(
            cropped,
            bounds.v_margin,
            bounds.v_margin,
            bounds.h_margin,
            bounds.h_margin,
            cv2.BORDER_CONSTANT,
            None,
            [0, 0, 0]
        )

        cv2.imshow("window", with_borders)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        key = cv2.waitKeyEx(1)
        if key & 0xFF == KEY_CODE_ESCAPE:
            break
        elif key & 0xFF == ord('i') or key & 0xFF == KEY_CODE_SPACE:
            runtime_settings.invert_colors = not runtime_settings.invert_colors
            persistence.save_runtime_settings(runtime_settings)
        elif key & 0xFF == ord('+') or key & 0xFF == KEY_CODE_ENTER:
            pan_zoom_state.scale_zoom(1.1)
            runtime_settings.zoom = pan_zoom_state.zoom_level
            persistence.save_runtime_settings(runtime_settings)
        elif key & 0xFF == ord('-') or key & 0xFF == KEY_CODE_BACKSPACE:
            pan_zoom_state.scale_zoom(1 / 1.1)
            runtime_settings.zoom = pan_zoom_state.zoom_level
            persistence.save_runtime_settings(runtime_settings)
        elif key & 0xFF == ord('f'):
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            runtime_settings.auto_focus = True
            persistence.save_runtime_settings(runtime_settings)
        elif key & 0xFF == ord('q'):
            if cap.get(cv2.CAP_PROP_AUTOFOCUS) == 1:
                cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            current = cap.get(cv2.CAP_PROP_FOCUS)
            runtime_settings.auto_focus = False
            runtime_settings.absolute_focus = max(0, current - config.camera_focus_step)
            cap.set(cv2.CAP_PROP_FOCUS, runtime_settings.absolute_focus)
            persistence.save_runtime_settings(runtime_settings)
        elif key & 0xFF == ord('w'):
            if cap.get(cv2.CAP_PROP_AUTOFOCUS) == 1:
                cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            current = cap.get(cv2.CAP_PROP_FOCUS)
            runtime_settings.auto_focus = False
            runtime_settings.absolute_focus = min(250, current + config.camera_focus_step)
            cap.set(cv2.CAP_PROP_FOCUS, runtime_settings.absolute_focus)
            persistence.save_runtime_settings(runtime_settings)
        elif key == KEY_CODE_ARROW_UP:
            pan_zoom_state.pan(0, -DELTA)
        elif key == KEY_CODE_ARROW_RIGHT:
            pan_zoom_state.pan(DELTA, 0)
        elif key == KEY_CODE_ARROW_DOWN:
            pan_zoom_state.pan(0, DELTA)
        elif key == KEY_CODE_ARROW_LEFT:
            pan_zoom_state.pan(-DELTA, 0)
        elif key != -1:
            print(key)
finally:
    cap.release()
    cv2.destroyAllWindows()
    touch_input_handler.stop()

