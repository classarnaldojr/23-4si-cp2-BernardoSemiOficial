import os
import os.path
import sys

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector


def resizeImage(img):
    return cv2.resize(img, (0, 0), None, 0.475, 0.475)

def desenharEmTela(img, text, origem, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(text), origem, font,0.7,color,2,cv2.LINE_AA)

TESOURA = "TESOURA"
PEDRA = "PEDRA"
PAPEL = "PAPEL"
JOGADANAOIDENTIFICADA = "Jogada não identificada"

TEMPLATEPAPEL = resizeImage(cv2.imread("papel.png", 0))
TEMPLATETESOURA = resizeImage(cv2.imread("tesoura.png", 0))
TEMPLATEPEDRA = resizeImage(cv2.imread("pedra.png", 0))

REVERTTEMPLATEPAPEL = cv2.flip(TEMPLATEPAPEL, -1)
REVERTTEMPLATETESOURA = cv2.flip(TEMPLATETESOURA, -1)
REVERTTEMPLATEPEDRA = cv2.flip(TEMPLATEPEDRA, -1)

PLAYERLEFT = "Jogador da esquerda"
PLAYERRIGHT = "Jogador da direita"

placar = [0, 0] # [PLAYER LEFT, PLAYER RIGHT]
colorBlack = [0, 0, 0]

lastMovePlayLeft = ""
lastMovePlayRight = ""
lastPlayerWin = ""
lastScoreView = ""

def movePlayerLeft(imgGray, imgRgb):
    matchPapel = cv2.matchTemplate(imgGray, TEMPLATEPAPEL, cv2.TM_SQDIFF_NORMED)
    matchTesoura = cv2.matchTemplate(imgGray, TEMPLATETESOURA, cv2.TM_SQDIFF_NORMED)
    matchPedra = cv2.matchTemplate(imgGray, TEMPLATEPEDRA, cv2.TM_SQDIFF_NORMED)

    minMatchValuePapel, _, positionMatchPapel, _ = cv2.minMaxLoc(matchPapel)
    minMatchValueTesoura, _, positionMatchTesoura, _ = cv2.minMaxLoc(matchTesoura)
    minMatchValuePedra, _, positionMatchPedra, _ = cv2.minMaxLoc(matchPedra)

    _, heigthTemplatePapel = TEMPLATEPAPEL.shape[::-1]
    _, heigthTemplateTesoura = TEMPLATETESOURA.shape[::-1]
    _, heigthTemplatePedra = TEMPLATEPEDRA.shape[::-1]
    
    # PAPEL
    if minMatchValuePapel < 0.019:
        drawPosition = (positionMatchPapel[0] , positionMatchPapel[1] + heigthTemplatePapel + 30)
        desenharEmTela(imgRgb, PAPEL, drawPosition, colorBlack)
        return [PAPEL, positionMatchPapel]
    
    # TESOURA
    if minMatchValueTesoura < 0.030:
        drawPosition = (positionMatchTesoura[0] , positionMatchTesoura[1] + heigthTemplateTesoura + 30)
        desenharEmTela(imgRgb, TESOURA, drawPosition, colorBlack)
        return [TESOURA, positionMatchTesoura]
    
    # PEDRA
    if minMatchValuePedra < 0.0098: 
        drawPosition = (positionMatchPedra[0] , positionMatchPedra[1] + heigthTemplatePedra + 30)
        desenharEmTela(imgRgb, PEDRA, drawPosition, colorBlack)
        return [PEDRA, positionMatchPedra]
    
    return [JOGADANAOIDENTIFICADA, [0, 0]]

def movePlayerRight(imgGray, imgRgb):
    matchPapel = cv2.matchTemplate(imgGray, REVERTTEMPLATEPAPEL, cv2.TM_SQDIFF_NORMED)
    matchTesoura = cv2.matchTemplate(imgGray, REVERTTEMPLATETESOURA, cv2.TM_SQDIFF_NORMED)
    matchPedra = cv2.matchTemplate(imgGray, REVERTTEMPLATEPEDRA, cv2.TM_SQDIFF_NORMED)

    minMatchValuePapel, _, positionMatchPapel, _ = cv2.minMaxLoc(matchPapel)
    minMatchValueTesoura, _, positionMatchTesoura, _ = cv2.minMaxLoc(matchTesoura)
    minMatchValuePedra, _, positionMatchPedra, _ = cv2.minMaxLoc(matchPedra)

    _, heigthTemplatePapel = REVERTTEMPLATEPAPEL.shape[::-1]
    _, heigthTemplateTesoura = REVERTTEMPLATETESOURA.shape[::-1]
    _, heigthTemplatePedra = REVERTTEMPLATEPEDRA.shape[::-1]
    
    # PAPEL
    if minMatchValuePapel < 0.019:
        drawPosition = (positionMatchPapel[0] , positionMatchPapel[1] + heigthTemplatePapel + 30)
        desenharEmTela(imgRgb, PAPEL, drawPosition, colorBlack)
        return [PAPEL, positionMatchPapel]
    
    # TESOURA
    if minMatchValueTesoura < 0.030:
        drawPosition = (positionMatchTesoura[0] , positionMatchTesoura[1] + heigthTemplateTesoura + 30)
        desenharEmTela(imgRgb, TESOURA, drawPosition, colorBlack)
        return [TESOURA, positionMatchTesoura]
    
    # PEDRA
    if minMatchValuePedra < 0.0098: 
        drawPosition = (positionMatchPedra[0] , positionMatchPedra[1] + heigthTemplatePedra + 30)
        desenharEmTela(imgRgb, PEDRA, drawPosition, colorBlack)
        return [PEDRA, positionMatchPedra]
    
    return [JOGADANAOIDENTIFICADA, [0, 0]]

def score(movePlayerLeft, movePlayerRight):
    
    # PLAYER LEFT WIN
    if (movePlayerLeft == TESOURA and movePlayerRight == PAPEL) or \
        (movePlayerLeft == PAPEL and movePlayerRight == PEDRA) or \
        (movePlayerLeft == PEDRA and movePlayerRight == TESOURA):
        placar[0] += 1
        scoreView = str("Placar: ") + str(placar)
        return  ["JOGADOR ESQUERDO VENCEU", scoreView]
    
    # PLAYER RIGHT WIN
    if (movePlayerLeft == PAPEL and movePlayerRight == TESOURA) or \
        (movePlayerLeft == PEDRA and movePlayerRight == PAPEL) or \
        (movePlayerLeft == TESOURA and movePlayerRight == PEDRA):
        placar[1] += 1
        scoreView = str("Placar: ") + str(placar)
        return ["JOGADOR DIREITO VENCEU", scoreView]
    
    scoreView = str("Placar: ") + str(placar)
    return ["* JOGADORES EMPATARAM *", scoreView]

def newRound(movePlayLeft, movePlayRight):
    global lastMovePlayLeft
    global lastMovePlayRight

    if movePlayLeft != lastMovePlayLeft or movePlayRight != lastMovePlayRight:
        lastMovePlayLeft = movePlayLeft
        lastMovePlayRight = movePlayRight
        return True
    return False

def image_da_webcam(img):
    global lastPlayerWin
    global lastScoreView

    imgScaled = resizeImage(img)
    imgGray = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2GRAY)

    imgWidth = imgScaled.shape[1]

    movePlayLeft, matchPositionLeft = movePlayerLeft(imgGray, imgScaled)
    movePlayRight, matchPositionRight = movePlayerRight(imgGray, imgScaled)

    isNewRound = newRound(movePlayLeft, movePlayRight)
        
    if isNewRound:
        playerWin, scoreView = score(movePlayLeft, movePlayRight)
        lastPlayerWin = playerWin
        lastScoreView = scoreView

    desenharEmTela(imgScaled, lastScoreView, (int(imgWidth / 2) - 120, 50), colorBlack)
    desenharEmTela(imgScaled, lastPlayerWin, (int(imgWidth / 2) - 190, 90), colorBlack)
    desenharEmTela(imgScaled, PLAYERLEFT, (matchPositionLeft[0], (matchPositionLeft[1] - 30)), colorBlack)
    desenharEmTela(imgScaled, PLAYERRIGHT, (matchPositionRight[0], (matchPositionRight[1] - 30)), colorBlack)
        
    return imgScaled

# vc = cv2.VideoCapture(0)
vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame)

    cv2.imshow("preview", img)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("preview")
vc.release()

print("                              ")
print("| ---------- FIM ---------- |")
print("| ------- PONTUAÇÃO ------- |")
print("                              ")
print(f"| {PLAYERLEFT} --> {placar[0]} |")
print(f"| {PLAYERRIGHT}  --> {placar[1]} |")
print("                              ")
print("| --------------------------|")