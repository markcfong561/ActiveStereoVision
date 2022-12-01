import cv2
import os
from ShowCorners import CheckerboardDetector
from FindCheckerboard import findCheckboard, orderPoints, findCorners
import numpy as np

def showImages(directory):
    keyPress = None
    checkerboardDetector = CheckerboardDetector()
    images = os.listdir(directory)
    for image in images:
        currentImage = cv2.imread(f"{directory}/{image}")
        gray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray,50,0.01,20)
        cornerPoints = np.int0(corners)

        threshold = 35

        rowOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, False)
        colOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, True)
        checkerboard = checkerboardDetector.findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), threshold)
        if checkerboard is not None:
            for row in checkerboard:
                for point in row:
                    x, y = point
                    cv2.circle(currentImage, (x,y), 4, color=(0,0,255), thickness=5)

        cv2.imshow("Checkerboard", currentImage)
        keyPress = cv2.waitKey(0)
        if keyPress == ord('d'):
            os.remove(f"{directory}/{image}")

def getCameraMatrix(directory):
    images = os.listdir(directory)
    A = np.zeros((48, 12))
    counter = 0
    for image in images:
        counter += 1
        currentImage = cv2.imread(f"{directory}/{image}")
        copyImage = currentImage.copy()
        gray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)

        corners = findCorners(currentImage)
        cornerPoints = np.int0(corners)

        threshold = 35

        rowOrderedPoints = orderPoints(cornerPoints, threshold, False)
        colOrderedPoints = orderPoints(cornerPoints, threshold, True)
        checkerboard = findCheckboard(rowOrderedPoints, colOrderedPoints, (4, 6), threshold)
        if checkerboard is not None:
            for row in checkerboard:
                for point in row:
                    y, x = point
                    cv2.circle(copyImage, (x,y), 4, color=(0,255,0), thickness=2)

        cv2.imshow("Image", copyImage)
        cv2.waitKey(0)
        if checkerboard:
            currentRow = checkerboard[0]
            print(currentRow)
            for i in range(24):
                floatI = float(i) * 20
                if i < 6:
                    currentRow = checkerboard[0]
                    x, y = currentRow[i]
                    point3D = [floatI, 0.0, 0.0]
                elif i < 12:
                    currentRow = checkerboard[1]
                    x, y = currentRow[i - 6]
                    point3D = [floatI - 6, 1.0, 0.0]
                elif i < 18:
                    currentRow = checkerboard[2]
                    x, y = currentRow[i - 12]
                    point3D = [floatI - 12, 2.0, 0.0]
                else:
                    currentRow = checkerboard[3]
                    x, y = currentRow[i - 18]
                    point3D = [floatI - 18, 3.0, 0.0]
                
                A[2*i][0:3] = A[2*i+1][4:7] = point3D
                A[2*i][3] = A[2*i+1][7] = 1
                A[2*i][8:11] = [value * -x for value in point3D]
                A[2*i+1][8:11] = [value * -y for value in point3D]
                A[2*i][11] = -x
                A[2*i+1][11] = -y

            print(A)
            eigvals, eigvecs = np.linalg.eig(A.T @ A)
            minEigvec = eigvecs[:, eigvals.argmin()]

            P = np.zeros((3,4))
            P[0] = minEigvec[0:4]
            P[1] = minEigvec[4:8]
            P[2] = minEigvec[8:12]

            print(P)
            break

def camMatrixFromCVCorners(directory):
    images = os.listdir(directory)
    A = np.zeros((48, 12))
    counter = 0
    for image in images:
        print(counter)
        counter += 1
        currentImage = cv2.imread(f"{directory}/{image}")
        gray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6,4),None)

        for i in range(24):
            pass
            



def main():
    directory = f"{os.getcwd()}/CornerPics"
    getCameraMatrix(directory=directory)
    # showImages(directory=directory)

if __name__ == "__main__":
    main()
