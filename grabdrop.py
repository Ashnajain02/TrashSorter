import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

appleImg = cv2.imread("images/apple1.png", cv2.IMREAD_UNCHANGED)
appleImg = cv2.resize(appleImg, (150, 150))

originx, originy = 200, 200

detector = HandDetector(detectionCon=0.65)

while True:
    success, screen = cap.read()
    screen = cv2.flip(screen, 1)
    hands, screen = detector.findHands(screen, flipType=False)

    #image region: 
    h, w, _ = appleImg.shape

    if hands:
        lmList = hands[0]['lmList'] #list of all the landmarks of the first hand detected
        length, info, screen = detector.findDistance(lmList[8][:2], lmList[12][:2], screen)
        #check if clicked
        if length < 60:
            cursor = lmList[8]
            #check if in region
            if (originx < cursor[0] < originx+w) and (originy < cursor[1] < originy+h):
                #print("inside image")
                originx, originy = cursor[0]-w//2, cursor[1]-h//2
    
        try: 
            screen = cvzone.overlayPNG(screen, appleImg, [originx, originy])
        except:
            pass
    
    cv2.imshow("Screen", screen)
    cv2.waitKey(1)


