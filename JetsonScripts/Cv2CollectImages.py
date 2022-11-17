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
    leftCam = cv2.VideoCapture(gstreamer_pipeline())

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    keyPress = None
    start = time.time()
    picNum = 0

    while keyPress != ord('q'):
        retImage, image = leftCam.read()
        chessboard = []
        if retImage:
            cv2.imshow("Chessboard", image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            retCorners, corners = cv2.findChessboardCorners(gray, (6,4),None)
            if retCorners and time.time - start > 1:
                corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
                cv2.imwrite(f"./CornerPics/CornerPicture_{picNum}.jpg", image)
                chessboard = cv2.drawChessboardCorners(image, (6, 4), corners2)
                picNum += 1
                start = time.time()
            else:
                chessboard = []
            # if chessboard:
            #     cv2.imshow("Checkerboard", chessboard)
            # else:
            #     cv2.imshow("Checkerboard", image)
            keyPress = cv2.waitKey(5)

if __name__ == "__main__":
    main()