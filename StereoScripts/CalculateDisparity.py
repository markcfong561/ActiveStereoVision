import numpy as np
import cv2
import time

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    leftCam = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0, flip_method=0), cv2.CAP_GSTREAMER)
    rightCam = cv2.VideoCapture(gstreamer_pipeline(sensor_id=1, flip_method=0), cv2.CAP_GSTREAMER)
    keyPress = None
    # stereo = cv2.StereoSGBM_create(numDisparities=32, blockSize=25)
    stereo = cv2.StereoBM_create(numDisparities=0, blockSize=5)#(numDisparities=32, blockSize=5)
    while keyPress != ord('q'):
        startTime = time.time()
        ret1, leftImage = leftCam.read()
        ret2, rightImage = rightCam.read()
        if ret1 and ret2:
            leftImage = cv2.cvtColor(leftImage, cv2.COLOR_BGR2GRAY)
            rightImage = cv2.cvtColor(rightImage, cv2.COLOR_BGR2GRAY)
            disparity = stereo.compute(leftImage, rightImage)
            distances = 776 * (57.3 / disparity)
            if (distances[270][480] > 0):
                print(distances[270][480])
            disparity = np.uint8(6400 * (disparity - disparity.min()) / (disparity.max() - disparity.min()))

            cv2.imshow('gray', disparity)
            keyPress = cv2.waitKey(5)
        # print(f"fps: {1 / (time.time() - startTime)}")

if __name__ == "__main__":
    main()