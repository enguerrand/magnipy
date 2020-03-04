import numpy as np
import cv2

DELTA = 10

cap = cv2.VideoCapture(0)

dx = 0
dy = 0
dw = 0
dh = 0

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def decrease(inval, min, delta=DELTA):
    outval = inval - delta
    if outval < min:
        return min
    else:
        return outval


def increase(inval, max, delta=DELTA):
    outval = inval + delta
    if outval > max:
        return max
    else:
        return outval


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Our operations on the frame come here
    h = height + dh
    w = width + dw

    cropped = frame[dy:dy + h, dx:dx + w]

    # Display the resulting frame
    cv2.imshow("window", cropped)

    key = cv2.waitKeyEx(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('+'):
        dw = decrease(dw, - width + 2 * DELTA, 2 * DELTA)
        dh = decrease(dh, - height + 2 * DELTA, 2 * DELTA)
        dx = increase(dx, -dw)
        dy = increase(dy, -dh)
    elif key & 0xFF == ord('-'):
        dw = increase(dw, 0, 2 * DELTA)
        dh = increase(dh, 0, 2 * DELTA)
        dx = decrease(dx, 0)
        dy = decrease(dy, 0)
    elif key == 65362:  # cursor up
        dy = decrease(dy, 0)
    elif key == 65363:  # cursor right
        dx = increase(dx, -dw)
    elif key == 65364:  # cursor down
        dy = increase(dy, -dh)
    elif key == 65361:  # cursor right
        dx = decrease(dx, 0)

    if dx < 0:
        print("grr")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()