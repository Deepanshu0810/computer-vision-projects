import cv2 as cv
import mediapipe as mp
import time

class PoseDetector:
    def __init__(self):
        self.mPose = mp.solutions.pose
        self.pose = self.mPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

        return lmList
    
def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture('./data/dancing.mp4')
    detector = PoseDetector()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        frame = detector.findPose(frame)
        lmList = detector.findPosition(frame)
        if len(lmList) != 0:
            print(lmList[1])

        cv.imshow('Frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()