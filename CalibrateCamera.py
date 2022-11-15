import cv2
from os import listdir
from ShowCorners import CheckerboardDetector
import numpy as np

def showImages(directory):
    checkerboardDetector = CheckerboardDetector()
    images = listdir(directory)
    print(images)
    for image in images:
        currentImage = cv2.imread(f"{directory}/{image}")
        cv2.imshow(currentImage)
        gray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray,50,0.01,20)
        cornerPoints = np.int0(corners)

        for cornerPoint in cornerPoints:
            y, x = cornerPoint.ravel()
            cv2.circle(image, (y, x), 4, color=(0,0,255), thickness=2)

        threshold = 35

        rowOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, False)
        colOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, True)
        checkerboard = checkerboardDetector.findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), threshold)
        if checkerboard is not None:
            for row in checkerboard:
                for point in row:
                    x, y = point
                    cv2.circle(currentImage, (x,y), 4, color=(0,0,255), thickness=2)

        cv2.imshow("Checkerboard", currentImage)

def main():
    showImages("./CornerPics")

if __name__ == "__main__":
    main()
