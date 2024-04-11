import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import pygame

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

class Trash():
    def __init__(self, posX, posY):
        self.img = cv2.imread("images/apple1.png", cv2.IMREAD_UNCHANGED)
        self.img = cv2.resize(self.img, (150, 150))
        self.posX = posX
        self.posY = posY
        self.size = self.img.shape[:2]
        self.recyclable = False

    def update(self, cursor):
        ox = self.posX
        oy = self.posY
        h, w = self.size
 
        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posX = cursor[0] - w // 2
            self.posY = cursor[1] - h // 2
            #self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2

def initializeImages():
    listTrash = []
    posX = 0
    posY = 0
    for i in range(3):
        listTrash.append(Trash(posX, posY))
        posX += 100
        posY += 100
    return listTrash


listTrash = initializeImages()
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
 
    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listTrash:
                imgObject.update(cursor)
 
    try:
        for imgObject in listTrash:
            # Draw for JPG image
            h, w = imgObject.size
            ox = imgObject.posX
            oy = imgObject.posY
            img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
    except:
        pass
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)




