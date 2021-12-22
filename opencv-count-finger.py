import os
import time
import lib.hand as htm

import cv2
import numpy as np

# cap = cv2.VideoCapture('video.mp4')
cap = cv2.VideoCapture(0)
folder_path = 'image/fingers'
lst = os.listdir(folder_path)
lst.sort()
lst_image = []
pTime = 0

for i in lst:
    image = cv2.imread(f"{folder_path}/{i}")
    lst_image.append(image)

detector = htm.handDetector(detectionCon=int(0.55))
fingerId = [4, 8, 12, 16, 20]
while True:
    # ret = FALSE: when camera has problem
    # capture video like image per second
    ret, frame = cap.read()
    # find hand
    frame = detector.findHands(frame)
    # detector position of finger
    lmList = detector.findPosition(frame, draw=False)
    print(lmList)
    fingers = []
    if len(lmList) != 0:
        # cho ngón cái so sánh theo trục x
        if lmList[fingerId[0]][1] < lmList[fingerId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # cho 4 ngón dài so sánh theo trục y
        for i in range(1, 5):
            if lmList[fingerId[i]][2] < lmList[fingerId[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

    # copy image finger to camera window
    h, w, c = lst_image[fingers.count(1) - 1].shape
    frame[0:h, 0:w] = lst_image[fingers.count(1) - 1]

    # draw number finger
    cv2.rectangle(frame, (0, 120), (150, 300), (0, 255, 0), -1)
    cv2.putText(frame, str(fingers.count(1)), (20, 260), cv2.FONT_ITALIC, 5, (255, 0, 0), 2)
    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (w + 50, 50), cv2.FONT_ITALIC, 1, (200, 122, 150), 2)

    cv2.imshow('Camera Window', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
