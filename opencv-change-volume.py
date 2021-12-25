from sys import platform
import os
import time
import lib.hand as htm
import math
import cv2
import numpy as np

# cap = cv2.VideoCapture('video.mp4')
cap = cv2.VideoCapture(0)
pTime = 0
detector = htm.handDetector(detectionCon=int(0.7))

while True:
    # ret = FALSE: when camera has problem
    # capture video like image per second
    ret, frame = cap.read()
    # find hand
    frame = detector.findHands(frame)
    # detector position of finger
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        # position of 2 finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # draw point in finger
        cv2.circle(frame, (x1, y1), 15, (255, 0, 100), -1)
        cv2.circle(frame, (x2, y2), 15, (255, 0, 100), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 100), 3)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(frame, (cx, cy), 15, (255, 0, 100), -1)

        # calc line of 2 finger
        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [25, 230], [0, 100])
        volBar = np.interp(length, [25, 230], [400, 150])
        if platform == "linux":
            import alsaaudio
            m = alsaaudio.Mixer()
            current_volume = m.getvolume() # Get the current Volume
            m.setvolume(int(vol)) # Set the volume to 70%.
            pass
        elif platform == "darwin":
            import osascript
            osascript.osascript("set volume output volume {}".format(vol))
        elif platform == "win32":
            pass

        if length < 25:
            cv2.circle(frame, (cx, cy), 15, (255, 100, 200), -1)

        cv2.rectangle(frame, (50, 150), (100, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volBar)), (100, 400), (0, 255, 0), -1)
        cv2.putText(frame, f"Volume: {int(vol)} %", (10, 450), cv2.FONT_ITALIC, 1, (250, 0, 0), 2)

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 40), cv2.FONT_ITALIC, 1, (200, 0, 150), 2)

    cv2.imshow('Camera Window', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
