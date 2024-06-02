import cv2
import HandTrackingMod as htm
import time
import math


pTime = 0
cTime = 0

wCam, hCam = 720, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector()

pinkey = False
ring = False
middle = False
pointer = False
thumb = False

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    hands = []

    i = 0
    while i<detector.numHands(img):
        lmList = detector.findPosition(img, handNo = i, draw = False)
        hands.append(lmList)
        i+=1


    cv2.circle(img, (600, 30), 15, (0, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (585, 65), (615, 95), (0, 0, 0), cv2.FILLED)
    cv2.circle(img, (600, 130), 15, (0, 0, 0), cv2.FILLED)
    cv2.circle(img, (600, 180), 15, (0, 0, 0), cv2.FILLED)
    cv2.circle(img, (600, 230), 15, (0, 0, 0), cv2.FILLED)

    if(len(hands) != 0):
        for i in range(len(hands)):
            print(i)
            for j in range(len(hands[i])):
                cv2.putText(img, f'{j}', (hands[i][j][1], hands[i][j][2]), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)



        # x1, y1 = lmList[4][1], lmList[4][2]
        # x2, y2 = lmList[8][1], lmList[8][2]

        # cx, cy = (x1+x2)//2, (y1+y2)//2

        # cv2.putText(img, f'{4}', (x1, y1), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        # cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 5, cv2.FILLED)
        # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # length = math.hypot(x2-x1, y2-y1)
        
        # if(length <=50):
        #     cv2.circle(img, (cx, cy), 15, (255, 255, 255), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
