import cv2
import numpy as np

# cap = cv2.VideoCapture('video.mp4')
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('video/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
while True:
    # ret = FALSE: when camera has problem
    # capture video like image per second
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.putText(frame, 'Hoang Hong Ha', (width//2 - 300, 100), font, 2, (23, 123, 233),  5)
    out.write(img)
    cv2.imshow('Camera Window', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
