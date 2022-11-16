import cv2
import os
from ShowCorners import CheckerboardDetector
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
    checkerboardDetector = CheckerboardDetector()
    images = os.listdir(directory)
    A = np.zeros((48, 12))
    counter = 0
    for image in images:
        print(counter)
        counter += 1
        currentImage = cv2.imread(f"{directory}/{image}")
        gray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray,50,0.01,20)
        cornerPoints = np.int0(corners)

        threshold = 35

        rowOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, False)
        colOrderedPoints = checkerboardDetector.orderPoints(cornerPoints, threshold, True)
        checkerboard = checkerboardDetector.findCheckboard(rowOrderedPoints, colOrderedPoints, (6, 4), threshold)
        if checkerboard:
            currentRow = checkerboard[0]
            for i in range(6):
                x, y = currentRow[i]
                point3D = [i, 0, 0]
                A[2*i][0:3] = A[2*i+1][4:7] = point3D
                A[2*i][3] = A[2*i+1][7] = 1
                A[2*i][8:11] = [value * -x for value in point3D]
                A[2*i+1][8:11] = [value * -y for value in point3D]
                A[2*i][11] = -x
                A[2*i+1][11] = -y
            for i in range(6, 12):
                x, y = currentRow[i - 6]
                point3D = [i - 6, 1, 0]
                A[2*i][0:3] = A[2*i+1][4:7] = point3D
                A[2*i][3] = A[2*i+1][7] = 1
                A[2*i][8:11] = [value * -x for value in point3D]
                A[2*i+1][8:11] = [value * -y for value in point3D]
                A[2*i][11] = -x
                A[2*i+1][11] = -y
            for i in range(12, 18):
                x, y = currentRow[i - 12]
                point3D = [i - 12, 2, 0]
                A[2*i][0:3] = A[2*i+1][4:7] = point3D
                A[2*i][3] = A[2*i+1][7] = 1
                A[2*i][8:11] = [value * -x for value in point3D]
                A[2*i+1][8:11] = [value * -y for value in point3D]
                A[2*i][11] = -x
                A[2*i+1][11] = -y
            for i in range(18, 24):
                x, y = currentRow[i - 18]
                point3D = [i - 18, 3, 0]
                A[2*i][0:3] = A[2*i+1][4:7] = point3D
                A[2*i][3] = A[2*i+1][7] = 1
                A[2*i][8:11] = [value * -x for value in point3D]
                A[2*i+1][8:11] = [value * -y for value in point3D]
                A[2*i][11] = -x
                A[2*i+1][11] = -y
            # print(A)
            eigvals, eigvecs = np.linalg.eig(A.T @ A)
            minEigvec = eigvecs[:, eigvals.argmin()]

            P = np.zeros((3,4))
            P[0] = minEigvec[0:4]
            P[1] = minEigvec[4:8]
            P[2] = minEigvec[8:12]

            print(P)
            



def main():
    getCameraMatrix(f"{os.getcwd()}/CornerPics")

if __name__ == "__main__":
    main()
