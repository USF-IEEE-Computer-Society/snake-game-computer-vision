import cvzone
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
import random

# set up video stream

# initialize detector

class SnakeGameClass():
    def __init__(self, appleImagePath):
        # initialize the snake
        self.gameOver = False

    def spawnAppleRandomly(self):
        # spawnApplyRandomly
        pass

    def update(self, imgMain, currentSnakeHead):
        if self.gameOver:
            cv2.putText(
                imgMain,
                "Game Over",
                [50, 80],
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3,
                thickness=5,
                color=(0, 100, 0)
            )
        else:
            pass
            # recalculate the snake

            # make snake have a length max

            # eat food
            #if rx - self.wApple // 2 < cx < rx + self.wApple // 2 and \
            #        ry - self.hApple // 2 < cy < ry + self.hApple // 2:

            # draw snake

            # draw food

            # Check for collision
        #     pts = np.array(self.pointsCoord[:-2], np.int32)
        #     pts = pts.reshape((-1, 1, 2))
        #     cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
        #     minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
        #     if -1 <= minDist <= 1:
        #         self.gameOver = True
        #         self.pointsCoord = []
        #         self.pointsDistances = []
        #         self.currentLength = 0
        #         self.allowedLength = 150
        #         self.previousHeadCoord = 0, 0
        #         self.spawnAppleRandomly()
        # return imgMain


# initialize the game
game = SnakeGameClass("apple.png")

while True:
    pass
    # read the videostream

    # identify hands

    # display video

    # wait for one second

img.release()