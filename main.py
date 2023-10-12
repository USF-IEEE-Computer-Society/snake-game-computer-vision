import cvzone
import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
import random

# get video stream from the web camera
videostream = cv2.VideoCapture(0)

# declare the resolution of the video
videostream.set(3, 1280)
videostream.set(4, 720)

# initialize future detector for hands
detector = HandDetector(detectionCon=0.8, maxHands=1)

# class that contains our entire game
class SnakeGameClass():
    # initialize the snake
    def __init__(self, appleImagePath):
        # whether the game is over
        self.gameOver = False

        # coordinates of the points (dots) that make our snake
        self.pointsCoord = []

        # distances between those points that make our snake
        self.pointsDistances = []

        # snake length
        self.currentLength = 0

        # maximum snake length (prevents snake from being infinitely long)
        self.allowedLength = 150

        # coordinates where the snake head was, for example, a second before
        self.previousHeadCoord = 0, 0

        # download image of apple
        imageApple = cv2.imread(appleImagePath, cv2.IMREAD_UNCHANGED)

        # get the image size and make it smaller
        widthApple = int(imageApple.shape[1] * 20 / 100)
        heightApple = int(imageApple.shape[0] * 20 / 100)

        # store the width and height as a tuple for convenience
        dim = (widthApple, heightApple)

        # create a method for the game that will store the apple image with smaller size
        self.imgApple = cv2.resize(imageApple, dim, interpolation=cv2.INTER_AREA)

        # create methods for the game to store the apple image size
        self.hApple, self.wApple, _ = self.imgApple.shape

        # coordinates of where apple was spawned
        self.appleCoord = 0, 0

        # method that spawns the apple in random position
        self.spawnAppleRandomly()

        # our score / points (how many apples our snake ate)
        self.score = 0

    # function that spawns apple in random coordinates x (left-right) and y (top-bottom)
    def spawnAppleRandomly(self):
        # for x we choose between 100 and 1000 because if we chose between 0 and 1280
        # (our resolution) apple could spawn on the edge
        # similarly for y we choose between 100 and 600 and not 0 and 720
        self.appleCoord = random.randint(100, 1000), random.randint(100, 600)

    # function that every some n amount of milliseconds calculates and draws all movements in our game
    # imgMain is our video from webcamera, currentSnakeHead is coordinates of our hand because that is where
    # our snake head should be now
    def update(self, imgMain, currentSnakeHead):
        # condition that checks whether game is over
        if self.gameOver:
            # text that shows "Game over"
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
            # recalculate the snake
            # store where snake was in px, py, and where it is now in cx, cy
            px, py = self.previousHeadCoord
            cx, cy = currentSnakeHead
            # add new coordinates of the snake head to array
            self.pointsCoord.append([cx, cy])
            # calculate distance between new coordinates of snake head and previous one and store it
            distance = math.hypot(cx - px, cy - py)
            self.pointsDistances.append(distance)
            # increase length of the snake (imagine that snake stretched)
            self.currentLength += distance
            # set that previous coordinates of the snake head are current coordinates of the head (because by this time
            # snake could already move more)
            self.previousHeadCoord = cx, cy

            # make snake have a length max
            # if our snake stretched too much to move
            if self.currentLength > self.allowedLength:
                # go through the parts of the snake
                for i, length in enumerate(self.pointsDistances):
                    # delete the part of the snake tail
                    self.currentLength -= length
                    self.pointsDistances.pop(i)
                    self.pointsCoord.pop(i)
                    # check again whether now snake is of good length
                    if self.currentLength < self.allowedLength:
                        break

            # eat food
            # coordinates of the apple
            rx, ry = self.appleCoord

            # check whether coordinates of the snake are the same as the coordinates around apple's center
            # in other words it checks whether snake is touching the apple
            if rx - self.wApple // 2 < cx < rx + self.wApple // 2 and \
                   ry - self.hApple // 2 < cy < ry + self.hApple // 2:
                # if snake touches apple, respawn apple to different random location
                self.spawnAppleRandomly()
                # allow snake to become longer
                self.allowedLength += 50
                # give a point for eating an apple
                self.score += 1

            # draw snake
            # if snake even exists (we could make a mistake in code, and snake would not exist, or we could have no hands in the frame)
            if self.pointsCoord:
                # go through points/dots (parts) of the snake
                for i, point in enumerate(self.pointsCoord):
                    # if the part of the snake is not its head (because head will always be where our hand is)
                    if i != 0:
                        # draw a line connecting 2 points of the snake (making it look like a snake)
                        cv2.line(imgMain, self.pointsCoord[i - 1], self.pointsCoord[i], (0, 100, 0), 20)
                # draw the head of the snake
                cv2.circle(img, self.pointsCoord[-1], 20, (0, 100, 0), cv2.FILLED)


            # draw food
            # get coordinates of the apple
            rx, ry = self.appleCoord

            # put image of apple on top of our video from webcamera
            imgMain = cvzone.overlayPNG(imgMain, self.imgApple, (rx - self.wApple // 2, ry - self.hApple // 2))
            # put text saying the current score on top of our video from webcamera
            cv2.putText(
                imgMain,
                str(self.score),
                [50, 80],
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3,
                thickness = 5,
                color=(0, 100, 0)
            )

            # Check for collision (snake head touches snake head)
            # use mathematical array to store parts of the snake
            pts = np.array(self.pointsCoord[:-2], np.int32)

            # rotate the array (needed for better check of collision)
            pts = pts.reshape((-1, 1, 2))
            # draw light green line that will represent skeleton of the snake (needed so snake does not think it collided
            # when snake head touches snake neck because snake head always touches its neck)
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            # check the distance between the coordinates of the head and the skeleton
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            # if the distance is too small, snake collided
            if -1 <= minDist <= 1:
                # set that game is over
                self.gameOver = True
                # reset entire game as it was
                self.pointsCoord = []
                self.pointsDistances = []
                self.currentLength = 0
                self.allowedLength = 150
                self.previousHeadCoord = 0, 0
                self.spawnAppleRandomly()
        # return our video from web camera with changes we made like putting their text with score, game over and apple
        return imgMain


# initialize the game from the class and give it the path to apple image
game = SnakeGameClass("apple.png")

# infinite loop, so the video from web camera is always displayed
while True:
    # make python process the videostream that we got from web camera
    success, img = videostream.read()

    # mirror the video so when a person plays, they do not get confused where is left and right
    img = cv2.flip(img, 1)

    # identify hands at the video stream, store in hands the hands, and in img our videostream
    hands, img = detector.findHands(img, flipType=False)

    # if hands were found
    if hands:
        # get the coordinates of the hand
        handCoordinates = hands[0]['lmList'][8][0:2]
        # make our game class update the game with new hands position
        # (in other words move the snake, check if it ate the apple and etc)
        img = game.update(img, handCoordinates)

    # display video from web camera to player (otherwise only python will see it)
    cv2.imshow("Image", img)

    # wait for one second before updating the video, so our computer does not try to update it every millesecond and
    # collapses
    key = cv2.waitKey(1)

# close the video, just in case if there is error
img.release()