from typing import List
import cv2
import collections
import math
import numpy as np

def distance(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def orderPoints(points: np.ndarray, yThreshold: int):
    rows = {}
    currentRow = []
    for point in points:
        x, y = point.ravel()
        currentYCord = y
        # Go through rows created, see if new point can go inside
        for yCord in rows.keys():
            if abs(y - yCord) < yThreshold:
                currentRow = rows.get(yCord)
                currentYCord = yCord
                break
        currentRow.append(point)
        rows[currentYCord] = currentRow
        currentRow = []
    for row in rows:
        rows[row] = sorted(rows[row], key=lambda x: x[0][0])
    return rows

def findCheckboard(cornerList: List):
    
    pass

def prettyPrintOrdered(orderedPoints):
    for element in orderedPoints:
        print(f"Row Number: {element} Num Points in row: {len(orderedPoints[element])} Points: {orderedPoints[element]}")

    print("-------------------------------")

def main():
    # Live Video
    video = cv2.VideoCapture(0)

    keyPress = None

    while keyPress != ord('q'):
        ret, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blankImg = np.zeros(image.shape)
        if ret:
            corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
            cornerPoints = np.int0(corners)

            for cornerPoint in cornerPoints:
                y, x = cornerPoint.ravel()
                cv2.circle(image, (y, x), 4, color=(0,0,255), thickness=10)

            orderedPoints = orderPoints(cornerPoints, 20)
            orderedPoints = collections.OrderedDict(sorted(orderedPoints.items()))

            # prettyPrintOrdered(orderedPoints)

            i = 1
            for row in orderedPoints:
                for point in orderedPoints[row]:
                    y, x = point.ravel()
                    cv2.putText(image, str(i), (y+10, x+10), cv2.FONT_HERSHEY_PLAIN, 2, color=(0, 0, 255), thickness=1)
                    i += 1
            
            cv2.imshow("Webcam", image)
            keyPress = cv2.waitKey(5)
        else:
            print("Error opening video feed")
    while keyPress != ord('q'):
        keyPress = cv2.waitKey(5)

    # Still image for testing
    # image = cv2.imread('Checkerboard.jpg')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
    # cornerPoints = np.int0(corners)
    # orderedPoints = orderPoints(cornerPoints, 20)
    # orderedPoints = collections.OrderedDict(sorted(orderedPoints.items()))
    # prettyPrintOrdered(orderedPoints)

    # for cornerPoint in cornerPoints:
    #     y, x = cornerPoint.ravel()
    #     cv2.circle(image, (y,x), 4, color=(0,0,255), thickness=5)

    # i = 1
    # for row in orderedPoints:
    #     for point in orderedPoints[row]:
    #         y, x = point.ravel()
    #         cv2.putText(image, str(i), (y+10, x+10), cv2.FONT_HERSHEY_PLAIN, 2, color=(0, 0, 255), thickness=1)
    #         i += 1

    # cv2.imshow("Checkboard", image)

    # while keyPress != ord('q'):
    #     keyPress = cv2.waitKey(0)

if __name__ == '__main__':
    main()