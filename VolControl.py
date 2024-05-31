import cv2 
import time
import numpy as np
import HandTrackingMod as htm
import math

wCam, hCam = 720, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)



pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)

detector = htm.HandDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)

    if(len(lmList) != 0):
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 15, cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        
        if(length <=50):
            cv2.circle(img, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

        #Volume Control

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        #volume.GetMute()
        #volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)



    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
