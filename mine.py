from random import randint
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# variables
fingers = []
is_played = bool()
player_choose = 0
detector = HandDetector(detectionCon=0.8, maxHands=1)

def cpu():
    global cpu_choose
    global is_won
    global is_draw

    cpu_choose = randint(1,3)
    
    if cpu_choose == player_choose:
        is_draw = True
        is_won = False
        
    elif cpu_choose == 1 and player_choose == 2:
        is_draw = False
        is_won = True

    elif cpu_choose == 2 and player_choose == 3:
        is_draw = False
        is_won = True

    else:
        is_draw = False
        is_won = False


while True:

    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    img = cv2.addWeighted(img, 0.2, img, 0.8, 0)
    lmList = detector

    if not is_played:
            cv2.putText(img, 'press P to play', (900, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 5)

    if hands:
        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        key = cv2.waitKey(1)
        
        if key == ord('p') and is_played == False:
            i = 0
            if sum(fingers1) == 0 or sum(fingers1) == 1:
                player_choose = 1
                is_played = True
                cpu()
            elif sum(fingers1) == 2 or sum(fingers1) == 3:      #>= 2 and sum(fingers) <= 3:
                player_choose = 3
                is_played = True
                cpu()
            elif sum(fingers1) == 4 or sum(fingers1) == 5:
                player_choose = 2 
                is_played = True
                cpu()

        if key == ord('r') and is_played == True:
            is_played = False


    if is_played:

        if is_draw:
            cv2.putText(img, 'draw', (900, 650), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 165, 255), 5)
        elif is_won:
            cv2.putText(img, 'you win', (900, 650), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 5)
        elif not is_won and not is_draw:
            cv2.putText(img, 'you lose', (900, 650), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 10, 255), 5)
        
        if player_choose == 1:
            cv2.putText(img, 'you: rock', (900, 610), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)
        if player_choose == 2:
            cv2.putText(img, 'you: paper', (900, 610), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)
        if player_choose == 3:
            cv2.putText(img, 'you: scissor', (900, 610), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)
        print(cpu_choose)

        if cpu_choose == 1:
            cv2.putText(img, 'cpu: rock', (900, 570), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)
        if cpu_choose == 2:
            cv2.putText(img, 'cpu: paper', (900, 570), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)
        if cpu_choose == 3:
            cv2.putText(img, 'cpu: scissor', (900, 570), cv2.FONT_HERSHEY_COMPLEX,
                    1, (228, 50, 0), 5)

        cv2.putText(img, 'press R to play again', (900, 530), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 255, 255), 5)        


    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
        
