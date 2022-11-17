import cv2

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
    while keyPress != ord('q'):
        ret, image = rightCam.read()

        if ret:
            cv2.imshow("Camera", image)
            keyPress = cv2.waitKey(5)
    pass

if __name__ == "__main__":
    main()