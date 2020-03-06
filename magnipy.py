import cv2
import sys
from screeninfo import get_monitors

from pan_zoom_state import PanZoomState


KEY_CODE_BACKSPACE = 8
KEY_CODE_ENTER = 13
KEY_CODE_ESCAPE = 27
KEY_CODE_SPACE = 32
KEY_CODE_ARROW_LEFT = 65361
KEY_CODE_ARROW_UP = 65362
KEY_CODE_ARROW_RIGHT = 65363
KEY_CODE_ARROW_DOWN = 65364

video_device = "/dev/video0"
if len(sys.argv) > 1:
    video_device = "/dev/" + sys.argv[1]

DELTA = 10

cap = cv2.VideoCapture(video_device)

try:
    ret, frame = cap.read()
    if frame is None:
        print("Failed to capture from device " + video_device + " => Aborting execution")
        sys.exit(-1)

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    display_width = get_monitors()[0].width
    display_height = get_monitors()[0].height
    inverted = False
    ratio = display_width / display_height

    height, width, channels = frame.shape
    pan_zoom_state = PanZoomState(width, height, 10, display_width, display_height)

    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape

        bounds = pan_zoom_state.compute_bounds()

        cropped = frame[bounds.dy:bounds.dy + bounds.height, bounds.dx:bounds.dx + bounds.width]

        if inverted:
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
            inverted = not inverted
        elif key & 0xFF == ord('+') or key & 0xFF == KEY_CODE_ENTER:
            pan_zoom_state.scale_zoom(1.1)
        elif key & 0xFF == ord('-') or key & 0xFF == KEY_CODE_BACKSPACE:
            pan_zoom_state.scale_zoom(1 / 1.1)
        elif key == KEY_CODE_ARROW_UP:  # cursor up
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
