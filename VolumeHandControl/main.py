import cv2 as cv
from HandTracking.HandTrackingModule import HandDetector
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

wCam = 640
hCam = 480

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
# volume.SetMasterVolumeLevel(-20.0, None)

cap = cv.VideoCapture(0)
detector = HandDetector()
cap.set(3, wCam)
cap.set(4, hCam)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(frame, (x1, y1), 10, (255, 0, 255), cv.FILLED)
        cv.circle(frame, (x2, y2), 10, (255, 0, 255), cv.FILLED)
        cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)

        cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 200], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv.circle(frame, (cx, cy), 10, (0, 255, 0), cv.FILLED)

        # print(lmList[4], lmList[8])



    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()