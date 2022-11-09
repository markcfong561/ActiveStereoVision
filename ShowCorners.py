from typing import List
import cv2
import math
import numpy as np
from skimage import feature
from itertools import compress

def distance(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def findCheckboard(cornerList: List):
    
    pass

def main():
    video = cv2.VideoCapture(0)

    keyPress = None

    while keyPress != ord('q'):
        ret, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if ret:
            corners = cv2.cornerHarris(gray, 2, 3, 0.04)

            cornerPoints = corners > 0.3 * corners.max()

            cornerPoints = np.argwhere(cornerPoints).tolist()

            i = 1
            for point1 in cornerPoints:
                for point2 in cornerPoints[i::1]:
                    if distance(point1, point2) < 10:
                        cornerPoints.remove(point2)
                i += 1

            for cornerPoint in cornerPoints:
                cv2.circle(image, (cornerPoint[1], cornerPoint[0]), 4, color=(0,0,255))
            
            cv2.imshow("Webcam", image)
            keyPress = cv2.waitKey(5)
        else:
            print("Error opening video feed")
    # while keyPress != ord('q'):
    #     keyPress = cv2.waitKey(5)

if __name__ == '__main__':
    main()