import cv2 as cv
from HandTracking.HandTrackingModule import HandDetector

wCam = 640
hCam = 480

cap = cv.VideoCapture(0)
detector = HandDetector()

cap.set(3, wCam)
cap.set(4, hCam)

tips = [4, 8, 12, 16, 20]

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    if len(lmList) != 0:
        fingerOpen = []

        # check right or left
        if lmList[17][1] > lmList[5][1]:
            # print("Right Hand")
            if lmList[tips[0]][1] < lmList[tips[0] - 1][1]:
                # print("Thumb Open")
                fingerOpen.append(1)
            else:
                # print("Thumb Close")
                fingerOpen.append(0)
            
        else:
            # print("Left Hand")
            if lmList[tips[0]][1] > lmList[tips[0] - 1][1]:
                # print("Thumb Open")
                fingerOpen.append(1)
            else:
                # print("Thumb Close")
                fingerOpen.append(0)


        for id in range(1, 5):
            if lmList[tips[id]][2] < lmList[tips[id] - 2][2]:
                # print(f"Finger {id} Open")
                fingerOpen.append(1)
            else:
                # print(f"Finger {id} Close")
                fingerOpen.append(0)

        # print(fingerOpen)
        count = fingerOpen.count(1)
        cv.putText(frame, f"Finger Count: {count}", (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        

    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()