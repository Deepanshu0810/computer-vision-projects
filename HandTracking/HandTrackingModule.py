import cv2 as cv
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    if id == 0:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    if id == 4:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    if id == 8:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    if id == 12:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    if id == 16:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    if id == 20:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        return lmList
    
def main():
    cap = cv.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cv.imshow("Image", img)
        if cv.waitKey(1)==ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()