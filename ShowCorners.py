from typing import List
import cv2
import numpy as np

def orderPoints(points: np.ndarray, threshold: int, byColumn: bool):
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
            for position in lines[:]:
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


def findCheckboard(rowList: dict[int, List], colList: dict[int, List], shape: tuple[int, int]):
    return None

def main():
    # Live Video
    # video = cv2.VideoCapture(0)
# 
    keyPress = None
# 
    # while keyPress != ord('q'):
    #     ret, image = video.read()
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     if ret:
    #         corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
    #         cornerPoints = np.int0(corners)

    #         for cornerPoint in cornerPoints:
    #             y, x = cornerPoint.ravel()
    #             cv2.circle(image, (y, x), 4, color=(0,0,255), thickness=2)

    #         rowOrderedPoints = orderPoints(cornerPoints, 20, False)
    #         rowOrderedPoints = collections.OrderedDict(sorted(rowOrderedPoints.items()))
    #         colOrderedPoints = orderPoints(cornerPoints, 20, True)
    #         colOrderedPoints = collections.OrderedDict(sorted(colOrderedPoints.items()))

    #         checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4))
    #         # print(topLeft)
    #         if checkboardCorners is not None:
    #             for row in checkboardCorners:
    #                 for point in row:
    #                     x, y = point.ravel()
    #                     cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)

    #         # prettyPrintOrdered(orderedPoints)
    #         # 
    #         cv2.imshow("Webcam", image)
    #         keyPress = cv2.waitKey(5)
    #     else:
    #         print("Error opening video feed")

    # Still image for testing
    image = cv2.imread('Checkerboard.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray,40,0.01,10)
    cornerPoints = np.int0(corners)
    rowOrderedPoints = orderPoints(cornerPoints, 30, False)
    # colOrderedPoints = orderPoints(cornerPoints, 30, True)

    i = 0
    for row in rowOrderedPoints:
        print(row)
        for point in row[1]:
            x, y = point
            cv2.circle(image, (x, y), 4, color=(0,0,255), thickness=5)
            cv2.putText(image, str(i), (x + 10, y + 10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255,255,255), thickness=1)
            i += 1
        i = 0

    # checkboardCorners = findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4))
            # print(topLeft)
    # if checkboardCorners is not None:
    #     for row in checkboardCorners:
    #         for point in row:
    #             x, y = point.ravel()
    #             cv2.circle(image, (x,y), 4, color=(0,255,0), thickness=2)

    cv2.imshow("Checkboard", image)

    while keyPress != ord('q'):
        keyPress = cv2.waitKey(0)

if __name__ == '__main__':
    main()