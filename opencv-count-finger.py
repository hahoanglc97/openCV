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
widthCam = int(cap.get(3))
heightCam = int(cap.get(4))


def countFinger(lmList, handNo=0):
    finger = []
    if handNo == 0:
        # cho ngón cái so sánh theo trục x
        if lmList[fingerId[0]][1] < lmList[fingerId[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)
    else:
        # cho ngón cái so sánh theo trục x
        if lmList[fingerId[0]][1] > lmList[fingerId[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)
    # cho 4 ngón dài so sánh theo trục y
    for i in range(1, 5):
        if lmList[fingerId[i]][2] < lmList[fingerId[i] - 2][2]:
            finger.append(1)
        else:
            finger.append(0)

    return finger


def drawNumberFingerLeft(frame, numberFinger=0):
    # copy image finger to camera window
    h, w, c = lst_image[numberFinger - 1].shape
    frame[0:h, 0:w] = lst_image[numberFinger - 1]

    # draw number finger
    cv2.rectangle(frame, (0, 120), (150, 300), (7, 61, 92), -1)
    cv2.putText(frame, str(numberFinger), (20, 260), cv2.FONT_ITALIC, 5, (197, 211, 219), 2)


def drawNumberFingerRight(frame, numberFinger=0):
    # copy image finger to camera window
    h, w, c = lst_image[numberFinger - 1].shape
    frame[0:h, (widthCam - w):widthCam] = lst_image[numberFinger - 1]

    # draw number finger
    cv2.rectangle(frame, (widthCam, 120), (widthCam-150, 300), (7, 61, 92), -1)
    cv2.putText(frame, str(numberFinger), (widthCam-120, 260), cv2.FONT_ITALIC, 5, (197, 211, 219), 2)

while True:
    # ret = FALSE: when camera has problem
    # capture video like image per second
    ret, frame = cap.read()
    # find hand
    frame = detector.findHands(frame)
    # detector position of finger
    lmListLeftHand = detector.findPosition(frame, handNo=0, draw=False)
    lmListRightHand = detector.findPosition(frame, handNo=1, draw=False)
    drawNumberFingerLeft(frame)
    drawNumberFingerRight(frame)

    if len(lmListLeftHand) != 0:
        fingerNumber = countFinger(lmListLeftHand, handNo=0)
        drawNumberFingerLeft(frame, numberFinger=fingerNumber.count(1))

    if len(lmListRightHand) != 0:
        fingerNumber = countFinger(lmListRightHand, handNo=1)
        drawNumberFingerRight(frame, numberFinger=fingerNumber.count(1))

    # show fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (150, 50), cv2.FONT_ITALIC, 1, (197, 211, 219), 2)

    cv2.putText(frame, 'Left Hand',  (5, 350), cv2.FONT_ITALIC, 1, (197, 211, 219), 2)
    cv2.putText(frame, 'Right Hand',  (widthCam-180, 350), cv2.FONT_ITALIC, 1, (197, 211, 219), 2)


    cv2.imshow('Camera Window', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
