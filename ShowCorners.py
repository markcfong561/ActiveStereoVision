from typing import List
import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import time

class CheckerboardDetector():

    def distance(self, point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def orderPoints(self, points: np.ndarray, threshold: int, byColumn: bool):
        lines = []
        currentLine = []
        for point in points:
            point = tuple(point[0])
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


    def findCheckboard(self, rowList: List[tuple[int, List]], colList: List[tuple[int, List]], shape: tuple[int, int], threshold: int):
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
                    pointPos = col[1].index(topLeft[0])
                    leftEdge = col[1][pointPos:pointPos + h]
                    break
            checkboard = []
            currentRow = 0
            for farLeft in leftEdge:
                while currentRow < len(rowList):
                    currentRow += 1
                    if farLeft in rowList[currentRow - 1][1]:
                        cornerPos = rowList[currentRow - 1][1].index(farLeft)
                        if cornerPos + w > len(rowList[currentRow - 1][1]):
                            return None
                        checkboard.append(rowList[currentRow - 1][1][cornerPos:cornerPos + w])
                        break
                    else:
                        return None
                if len(checkboard) == h:
                    break
            return checkboard
        return None

    def refineCheckerboard(self, checkerboard: List[tuple[int, List]]):
        checkerboardSubPix = []
        for row in checkerboard:
            avgChangeInX = np.mean(row[:][0])
            avgChangeInY = np.mean(row[:][1])
            x1, y1 = row[0]
            newRow = []
            for i in range(len(row)):
                newRow.append((x1 + avgChangeInX * i, y1 + avgChangeInY * i))
            checkerboardSubPix.append(newRow)
        return checkerboardSubPix

def main():
    # Live Video
    video = cv2.VideoCapture(0)
    checkerboardDetector = CheckerboardDetector()
# 
    keyPress = None
#     startTime = time.time()
#     picNum = 0
# # 
#     while keyPress != ord('q'):
#         ret, image = video.read()
#         previewPic = np.copy(image)
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         if ret:
#             corners = cv2.goodFeaturesToTrack(gray,50,0.01,20)
#             cornerPoints = np.int0(corners)

#             for cornerPoint in cornerPoints:
#                 y, x = cornerPoint.ravel()
#                 cv2.circle(previewPic, (y, x), 4, color=(0,0,255), thickness=2)

#             threshold = 35
#             rowOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, False)
#             colOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, True)

#             i = 0
#             for row in rowOrderedPoints:
#                 for point in row[1]:
#                     x, y = point
#                     cv2.circle(previewPic, (x, y), 4, color=(0,0,255), thickness=5)
#                     cv2.putText(previewPic, str(i), (x + 10, y + 10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,0,255), thickness=1)
#                     i += 1
#                 i = 0

#             checkboardCorners = checkerboardDetector.findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), threshold)
#             if checkboardCorners is not None:
#                 for row in checkboardCorners:
#                     for point in row:
#                         x, y = point
#                         cv2.circle(previewPic, (x,y), 4, color=(0,255,0), thickness=2)
#                 if time.time() - startTime > 1:
#                     cv2.imwrite(f"./CornerPics/CornerPicture_{picNum}.jpg", image)
#                     picNum += 1
#                     startTime = time.time()

#             # prettyPrintOrdered(orderedPoints)
#             # 
#             cv2.imshow("Webcam", previewPic)
#             keyPress = cv2.waitKey(5)
#         else:
#             print("Error opening video feed")

    # Still image for testing
    # image = cv2.imread('Checkerboard.jpg')
    image = cv2.imread(f"{os.getcwd()}/CornerPics/CornerPicture_0.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray,50,0.01,20)
    cornerPoints = np.int0(corners)
    rowOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, 30, False)
    colOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, 30, True)

    i = 0
    for row in rowOrderedPoints:
        for point in row[1]:
            x, y = point
            cv2.circle(image, (x, y), 4, color=(0,0,255), thickness=5)
            cv2.putText(image, str(i), (x + 10, y + 10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,0,255), thickness=1)
            i += 1
        i = 0

    checkboardCorners = checkerboardDetector.findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), 30)
    refinedCheckerboardCorners = checkerboardDetector.refineCheckerboard(checkboardCorners)
    print(checkboardCorners)
    print(refinedCheckerboardCorners)
    if checkboardCorners is not None:
        for row in checkboardCorners:
            for point in row:
                x, y = point
                cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)

    cv2.imshow("Checkboard", image)

    while keyPress != ord('q'):
        keyPress = cv2.waitKey(0)

if __name__ == '__main__':
    main()