import numpy as np
import cv2
import sys
from screeninfo import get_monitors

from pan_zoom_state import PanZoomState

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


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        height, width, channels = frame.shape

        # Our operations on the frame come here
        bounds = pan_zoom_state.compute_bounds()

        cropped = frame[bounds.dy:bounds.dy + bounds.height, bounds.dx:bounds.dx + bounds.width]

        if inverted:
            cropped = cv2.bitwise_not(cropped)

        with_borders = cv2.copyMakeBorder(
            cropped, bounds.v_margin, bounds.v_margin, bounds.h_margin, bounds.h_margin, cv2.BORDER_CONSTANT, None, [0, 0, 0]
        )

        # Display the resulting frame
        cv2.imshow("window", with_borders)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        key = cv2.waitKeyEx(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('i'):
            inverted = not inverted
        if key & 0xFF == ord('+'):
            pan_zoom_state.scale_zoom(1.1)
        elif key & 0xFF == ord('-'):
            pan_zoom_state.scale_zoom(1 / 1.1)
        elif key == 65362:  # cursor up
            pan_zoom_state.pan(0, -DELTA)
        elif key == 65363:  # cursor right
            pan_zoom_state.pan(DELTA, 0)
        elif key == 65364:  # cursor down
            pan_zoom_state.pan(0, DELTA)
        elif key == 65361:  # cursor right
            pan_zoom_state.pan(-DELTA, 0)

finally:
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
