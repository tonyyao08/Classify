import cv2
import time
import logging


class Detector:

    def __init__(self):
        self.prevDetectionTime = None
        self.interval = 2
        self.captureKey = 99

    def doCapture(self, frame):
        """
        Do capture is where the image gets captured and the captured frame is then sent
        sent to the s3 bucket. This function is being run in a continuous loop and the
        key press of the letter C triggers an image capture.
        """
        h_i, w_i, _ = frame.shape
        # resize window
        rs = .78
        window_width = int(w_i * (rs-.4))
        window_height = int(h_i * rs-.2)

        cv2.namedWindow('Live Feed', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Live Feed', window_width, window_height)
        cv2.imshow("Live Feed", frame)
        key = cv2.waitKey(5)
        if self.prevDetectionTime is None and key == self.captureKey:
            self.prevDetectionTime = time.time()
            return True
        elif key == self.captureKey and time.time() - self.prevDetectionTime >= self.interval:
            self.prevDetectionTime = time.time()
            return True
        return False
