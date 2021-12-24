"""
Hand Module

"""

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawingStyles = mp.solutions.drawing_styles

    def getLabel(self, index):
        text = None
        if len(self.results.multi_handedness) == 1:
            # label = self.results.multi_handedness[0].classification[0].label
            score = self.results.multi_handedness[0].classification[0].score
            text = '{} {}'.format('Left', round(score, 2))
        else:
            for idx, classification in enumerate(self.results.multi_handedness):
                if classification.classification[0].index == index:
                    label = classification.classification[0].label
                    score = classification.classification[0].score
                    text = '{} {}'.format(label, round(score, 2))
        return text

    def findHands(self, img, draw=True):
        h, w, c = img.shape
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)
        # self.results.multi_hand_landmarks collection position of 21 point in hand
        if self.results.multi_hand_landmarks:
            for num, handLms in enumerate(self.results.multi_hand_landmarks):
                if draw:
                    x_max = 0
                    y_max = 0
                    x_min = w
                    y_min = h
                    # lm is position of one point in 21 point in the hand
                    # value in [0,1]
                    for lm in handLms.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)
                        if x > x_max:
                            x_max = x
                        if x < x_min:
                            x_min = x
                        if y > y_max:
                            y_max = y
                        if y < y_min:
                            y_min = y
                    cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 200, 255), 2)
                    if num == 1:
                        cv2.putText(img,
                                    self.getLabel(num),
                                    (x_max + 20, y_min - 30),
                                    cv2.FONT_ITALIC,
                                    1, (0, 200, 255), 2)
                    else:
                        cv2.putText(img,
                                    self.getLabel(num),
                                    (x_min - 20, y_min - 30),
                                    cv2.FONT_ITALIC,
                                    1, (0, 200, 255), 2)
                    # print(labelHand)
                    # draw 3D model  only for image
                    # self.mpDraw.plot_landmarks(handLms)
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS,
                                               self.drawingStyles.get_default_hand_landmarks_style(),
                                               self.drawingStyles.get_default_hand_connections_style())
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            for num, myHand in enumerate(self.results.multi_hand_landmarks):
                if num == handNo:
                    for id, lm in enumerate(myHand.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
