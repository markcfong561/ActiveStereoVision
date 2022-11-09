import cv2
import numpy as np
from skimage import feature

def main():
    video = cv2.VideoCapture(0)

    keyPress = None

    while keyPress != ord('q'):
        ret, image = video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if ret:
            corners = cv2.cornerHarris(gray, 2, 3, 0.04)

            cornerPoints = corners > 0.05 * corners.max()

            

            image[corners > 0.05 * corners.max()]=[0,0,255]
            
            cv2.imshow("Webcam", image)
            keyPress = cv2.waitKey(5)
        else:
            print("Error opening video feed")
    pass

if __name__ == '__main__':
    main()