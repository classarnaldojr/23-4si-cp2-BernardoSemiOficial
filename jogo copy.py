import os
import os.path
import sys

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=2, detectionCon=0.1, minTrackCon=0.5)
# detector = HandDetector(maxHands=2)

TESOURA = "TESOURA"
PEDRA = "PEDRA"
PAPEL = "PAPEL"

PLAYERLEFT = "Jogador 1"
PLAYERRIGHT = "Jogador 2"

tesoura = [0, 1, 1, 0, 0]
pedra = [0, 0, 0, 0, 0]
papel = [1, 1, 1, 1, 1]

placar = [0, 0] # [PLAYER LEFT, PLAYER RIGHT]
colorBlack = [0, 0, 0]

def escreve_texto(img, text, origem, color):
    """ faz a cruz no ponto cx cy"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(text), origem, font,1,color,2,cv2.LINE_AA)

def image_da_webcam(img):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    imgScaled = cv2.resize(img, (0, 0), None, 0.475, 0.475)
    # imgScaled = img
    imgView = imgScaled.copy()

    imgWidth = imgScaled.shape[1]

    hands, img = detector.findHands(imgScaled)

    # if hands:
    #     handLeft = hands[0]
    #     fingersLeft = detector.fingersUp(handLeft)
    #     print("Mãos:", len(hands), fingersLeft)

    if hands and len(hands) == 2:
        playerLeft = None
        playerRight = None
        handLeft = hands[0]
        handRight = hands[1]
        xLeft, yLeft, wLeft, hLeft = handLeft['bbox']
        xRight, yRight, wRight, hRight = handRight['bbox']
        fingersLeft = detector.fingersUp(handLeft)
        fingersRight = detector.fingersUp(handRight)

        print(fingersLeft, fingersRight)

        if fingersLeft == pedra:
            playerLeft = PEDRA
        elif fingersLeft == papel:
            playerLeft = PAPEL
        elif fingersLeft == tesoura:
            playerLeft = TESOURA
        
        if fingersRight == pedra:
            playerRight = PEDRA
        elif fingersRight == papel:
            playerRight = PAPEL
        elif fingersRight == tesoura:
            playerRight = TESOURA

        print(playerLeft, playerRight)

        # PLAYER LEFT WIN
        if (playerLeft == TESOURA and playerRight == PAPEL) or \
            (playerLeft == PAPEL and playerRight == PEDRA) or \
            (playerLeft == PEDRA and playerRight == TESOURA):
            placar[0] += 1
        
        # PLAYER RIGHT WIN
        if (playerLeft == PAPEL and playerRight == TESOURA) or \
            (playerLeft == PEDRA and playerRight == PAPEL) or \
            (playerLeft == TESOURA and playerRight == PEDRA):
            placar[1] += 1

        escreve_texto(imgView, str("Placar: ") + str(placar), (int(imgWidth / 2) - 100, 50), colorBlack)
        escreve_texto(imgView, PLAYERLEFT, (xLeft, (yLeft - 50)), colorBlack)
        escreve_texto(imgView, PLAYERRIGHT, (xRight, (yRight - 50)), colorBlack)

    return [imgView, img]

# vc = cv2.VideoCapture(0)
vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img, teste = image_da_webcam(frame)

    cv2.imshow("preview", img)
    cv2.imshow("teste", teste)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("preview")
cv2.destroyWindow("teste")
vc.release()