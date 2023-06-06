import cv2
import mediapipe as mp
from pynput.keyboard import Controller
from time import sleep
import math

camIndex = 0
cap = cv2.VideoCapture(camIndex)
mpHands = mp.solutions.hands
Hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

keyboard = Controller()


class Store():
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text


def draw(img, storedVar):
    for button in storedVar:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 43), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    return img


StoredVar = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        StoredVar.append(Store([60 * j + 10, 60 * i + 10], [50, 50], key))

while cap.isOpened():
    success_, img = cap.read()
    cvtImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(cvtImg)
    lmList = []

    if results.multi_hand_landmarks:
        for img_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, img_in_frame, mpHands.HAND_CONNECTIONS)
        for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([cx, cy])

    if lmList:
        for button in StoredVar:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 255), cv2.FILLED)
                x1, y1 = lmList[8][0], lmList[8][1]
                x2, y2 = lmList[12][0], lmList[12][1]
                l = math.hypot(x2 - x1 - 30, y2 - y1 - 30)
                print(l)
                ## when clicked
                if not l > 63:
                    keyboard.press(button.text)
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                    sleep(0.15)

    img = draw(img, StoredVar)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) == 113:  # Q=113
        break
