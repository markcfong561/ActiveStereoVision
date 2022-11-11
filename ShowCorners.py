from typing import List
import cv2
import collections
import math
import numpy as np

def distance(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def orderPoints(points: np.ndarray, threshold: int, byColumn: bool):
    rows = {}
    currentRow = []
    for point in points:
        x, y = point.ravel()
        if byColumn:
            interestCord = x
        else:
            interestCord = y
        # Go through rows created, see if new point can go inside
        for position in rows.keys():
            if abs(interestCord - position) < threshold:
                currentRow = rows.get(position)
                interestCord = position
                break
        currentRow.append(point)
        rows[interestCord] = currentRow
        currentRow = []
    # Sort points left/right or up/down
    for row in rows:
        rows[row] = sorted(rows[row], key=lambda x: x[0][1 * byColumn])
    return rows


def findCheckboard(rowList: dict[int, List], colList: dict[int, List], shape: tuple[int, int]):
    w, h = shape
    eligableRows = []
    eligableCols = []
    for row in rowList:
        if len(rowList[row]) >= w:
            eligableRows.append(rowList[row])
    if len(eligableRows) >= h:
        for col in colList:
            if len(colList[col]) >= h:
                eligableCols.append(colList[col])
        if len(eligableCols) >= w:
            firstInRows = [tuple(point.tolist()[0]) for point in eligableRows[:][:][0]]
            firstInCols = [tuple(point.tolist()[0]) for point in eligableCols[:][:][0]]
            topLeftList = list(set(firstInRows) & set(firstInCols))
            if len(topLeftList) > 0:
                topLeft = topLeftList[0]
                firstRow = list(rowList.keys())[(np.abs(np.subtract(list(rowList.keys()), topLeft[0]))).argmin()]
                checkboardList = []
                i = 0
                foundRow = False
                for row in rowList.keys():
                    if row == firstRow:
                        foundRow = True
                    if foundRow:
                        checkboardList.append(rowList[row])
                        i += 1
                    if i == h:
                        break
                return checkboardList
    return None

def prettyPrintOrdered(orderedPoints):
    for element in orderedPoints:
        print(f"Row Number: {element} Num Points in row: {len(orderedPoints[element])} Points: {orderedPoints[element]}")

    print("-------------------------------")

def main():
    # Live Video
    video = cv2.VideoCapture(0)
# 
    keyPress = None
# 
    while keyPress != ord('q'):
        ret, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if ret:
            corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
            cornerPoints = np.int0(corners)

            for cornerPoint in cornerPoints:
                y, x = cornerPoint.ravel()
                cv2.circle(image, (y, x), 4, color=(0,0,255), thickness=2)

            rowOrderedPoints = orderPoints(cornerPoints, 20, False)
            rowOrderedPoints = collections.OrderedDict(sorted(rowOrderedPoints.items()))
            colOrderedPoints = orderPoints(cornerPoints, 20, True)
            colOrderedPoints = collections.OrderedDict(sorted(colOrderedPoints.items()))

            checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4))
            # print(topLeft)
            if checkboardCorners is not None:
                for row in checkboardCorners:
                    for point in row:
                        x, y = point.ravel()
                        cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)

            # prettyPrintOrdered(orderedPoints)
            # 
            cv2.imshow("Webcam", image)
            keyPress = cv2.waitKey(5)
        else:
            print("Error opening video feed")

    # Still image for testing
    # image = cv2.imread('Checkerboard.jpg')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
    # cornerPoints = np.int0(corners)
    # rowOrderedPoints = orderPoints(cornerPoints, 30, False)
    # rowOrderedPoints = collections.OrderedDict(sorted(rowOrderedPoints.items()))
    # colOrderedPoints = orderPoints(cornerPoints, 30, True)
    # colOrderedPoints = collections.OrderedDict(sorted(colOrderedPoints.items()))
    # # prettyPrintOrdered(orderedPoints)

    # for cornerPoint in cornerPoints:
    #     x, y = cornerPoint.ravel()
    #     cv2.circle(image, (x,y), 4, color=(0,0,255), thickness=5)

    # i = 1
    # for row in rowOrderedPoints:
    #     for point in rowOrderedPoints[row]:
    #         x, y = point.ravel()
    #         cv2.circle(image, (x,y), 4, color=(0,0,255), thickness=5)
    #         cv2.putText(image, str(i), (x+10, y+10), cv2.FONT_HERSHEY_PLAIN, 2, color=(0, 0, 255), thickness=1)
    #         i += 1
    #     i = 1

    # topLeft = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4))
    # print(topLeft)
    # x, y = topLeft
    # cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=5)

    # cv2.imshow("Checkboard", image)

    # while keyPress != ord('q'):
    #     keyPress = cv2.waitKey(0)

if __name__ == '__main__':
    main()