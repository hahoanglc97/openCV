import cv2
import numpy as np

# cap = cv2.VideoCapture('video.mp4')
cap = cv2.VideoCapture(0)
while True:
    # ret = FALSE: when camera has problem
    # capture video like image per second
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # draw line
    # [image,start,end,color,width-line]
    # img = cv2.line(frame, (0, 0), (width, height), (0, 0, 0), 5)
    # img = cv2.line(frame, (0, height), (width, 0), (125, 55, 255), 5)

    # draw rectangle
    # img = cv2.rectangle(frame, (0, 0), (width//2, height//2), (0, 0, 0), -1)

    # draw circle
    # img = cv2.circle(frame, (width//2, height//2), 120, (0, 0, 0), -1)

    # draw text
    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.putText(frame, 'Hoang Hong Ha', (width//2 - 300, 100), font, 2, (23, 123, 233),  5)
    cv2.imshow('Camera Window', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
