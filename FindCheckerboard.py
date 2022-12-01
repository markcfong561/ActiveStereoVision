from typing import List
import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
import os
from scipy.ndimage import gaussian_filter
import time

def distance(point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def findCorners(image):
    checkerboard = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(float)

    stdI = 1.0
    stdD = .7
    a = .05

    Ix = gaussian_filter(checkerboard, stdD, order=[1, 0])
    Iy = gaussian_filter(checkerboard, stdD, order=[0, 1])
    Ixy = Ix * Iy

    gIx2 = gaussian_filter(Ix ** 2, stdI)
    gIy2 = gaussian_filter(Iy ** 2, stdI)
    gIxy = gaussian_filter(Ixy, stdI)

    R = (gIx2 * gIy2 - gIxy ** 2) - (a * ((gIx2 + gIy2) ** 2))

    thresholdedR = R * (R >= 9e4)

    maxSuppR = nonMaxSupp(thresholdedR).astype(np.uint8)

    positions = np.argwhere(maxSuppR == 1)
    # print(positions)

    # plt.imshow(checkerboard, 'gray')
    # plt.plot(positions[:,1], positions[:,0], 'ro')
    # plt.show()
    return positions

def nonMaxSupp(image: np.ndarray):
    maxSuppR = np.zeros(image.shape)
    for x in range(1, image.shape[1] - 1):
        for y in range(1, image.shape[0] - 1):
            if isUniqueMax(image, x, y):
                maxSuppR[y,x] = 1
    return maxSuppR

def isUniqueMax(image: np.ndarray, x, y):
    maximum = np.max(image[y-1:y+2,x-1:x+2])

    for xCheck in range(x - 1, x + 2):
        for yCheck in range(y - 1, y + 2):
            if image[yCheck, xCheck] == maximum and (yCheck != y or xCheck != x):
                return False

    return True

def orderPoints(points: np.ndarray, threshold: int, byColumn: bool):
    lines = []
    currentLine = []
    for point in points:
        point = tuple(point)
        x, y = point
        if byColumn:
            interestCord = x
        else:
            interestCord = y
        # Go through rows created, see if new point can go inside
        if lines:
            for position in lines:
                if abs(interestCord - position[0]) < threshold:
                    lines.remove(position)
                    currentLine = position
                    break
        if not currentLine:
            currentLine = (interestCord, [])
        currentLine[1].append(point)
        lines.append(currentLine)
        currentLine = []
    # # Sort points left/right or up/down
    lines = sorted(lines, key=lambda x: x[0])
    finalLines = []
    for line in lines:
        asList = list(line[1])
        asList = sorted(asList, key=lambda x: x[1 * int(byColumn)])
        finalLines.append(tuple([line[0], asList]))
    finalLines = sorted(finalLines, key=lambda x: x[0])
    return finalLines


def findCheckboard(rowList: List[tuple[int, List]], colList: List[tuple[int, List]], shape: tuple[int, int], threshold: int):
    w, h = shape
    eligableRows = []
    for row in rowList:
        if len(row[1]) >= w:
            eligableRows.append(row)
    if len(eligableRows) < h:
        return None
    eligableCols = []
    for col in colList:
        if len(col[1]) >= h:
            eligableCols.append(col)
    if len(eligableCols) < w:
        return None
    possibleRowCorners = []
    possibleColCorners = []
    for row in eligableRows:
        possibleRowCorners.extend(row[1][0:3])
    for col in eligableCols:
        possibleColCorners.extend(col[1][0:3])
    
    topLeft = list(set(possibleRowCorners) & set(possibleColCorners))
    if topLeft:
        leftEdge = []
        for col in eligableCols:
            if topLeft[0] in col[1]:
                leftEdge = col[1]
                break
        checkboard = []
        currentRow = 0
        for farLeft in leftEdge:
            while currentRow < len(rowList):
                currentRow += 1
                if farLeft in rowList[currentRow - 1][1]:
                    cornerPos = rowList[currentRow - 1][1].index(farLeft)
                    checkboard.append(rowList[currentRow - 1][1][cornerPos:cornerPos + w])
                    break
                else:
                    return None
            if len(checkboard) == h:
                break
        return checkboard
    return None

def main():
    # Live Video
#     video = cv2.VideoCapture(0)
# # 
#     keyPress = None
#     startTime = time.time()
#     picNum = 0
# # 
#     while keyPress != ord('q'):
#         ret, image = video.read()
#         imCopy = image.copy()
#         if ret:
#             cornerPoints = findCorners(image)

#             for cornerPoint in cornerPoints:
#                 y, x = cornerPoint.ravel()
#                 cv2.circle(image, (x, y), 4, color=(0,0,255), thickness=2)

#             threshold = 35
#             rowOrderedPoints = orderPoints(cornerPoints, threshold, False)
#             colOrderedPoints = orderPoints(cornerPoints, threshold, True)

#             checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), threshold)
#             if checkboardCorners is not None:
#                 for row in checkboardCorners:
#                     for point in row:
#                         y, x = point
#                         cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)
#                 if time.time() - startTime > 1:
#                     cv2.imwrite(f"./CornerPics/CornerPicture_{picNum}.jpg", imCopy)
#                     picNum += 1
#                     startTime = time.time()

#             # prettyPrintOrdered(orderedPoints)
#             # 
#             cv2.imshow("Webcam", image)
#             keyPress = cv2.waitKey(5)
#         else:
#             print("Error opening video feed")

    # Still image for testing
    # image = cv2.imread('Checkerboard.jpg')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
    # cornerPoints = np.int0(corners)
    # rowOrderedPoints = orderPoints(cornerPoints, 30, False)
    # colOrderedPoints = orderPoints(cornerPoints, 30, True)

    # i = 0
    # for row in rowOrderedPoints:
    #     for point in row[1]:
    #         x, y = point
    #         cv2.circle(image, (x, y), 4, color=(0,0,255), thickness=5)
    #         cv2.putText(image, str(i), (x + 10, y + 10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,0,255), thickness=1)
    #         i += 1
    #     i = 0

    # checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), 30)
    # print(checkboardCorners)
    # if checkboardCorners is not None:
    #     for row in checkboardCorners:
    #         for point in row:
    #             x, y = point
    #             cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)

    # cv2.imshow("Checkboard", image)

    # while keyPress != ord('q'):
    #     keyPress = cv2.waitKey(0)
    for imageName in os.listdir(f"{os.getcwd()}/CornerPics"):
        image = cv2.imread(f"./CornerPics/{imageName}")
        rgbIm = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cornerPoints = findCorners(image)
        newCornerPoints = []
        for point1 in cornerPoints:
            if all(distance(tuple(point1), tuple(point2)) > 5 for point2 in newCornerPoints):
                newCornerPoints.append(point1)
        cornerPoints = newCornerPoints

        rowOrderedPoints = orderPoints(cornerPoints, 30, False)
        colOrderedPoints = orderPoints(cornerPoints, 30, True)
        checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (4, 6), 30)
        if checkboardCorners is not None:
            for row in checkboardCorners:
                for point in row:
                    y, x = point
                    cv2.circle(rgbIm, (x,y), 4, color=(0,255,0), thickness=2)

        plt.imshow(rgbIm)
        plt.show()

if __name__ == '__main__':
    main()