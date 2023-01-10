from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import logging

# This is where the camera gets initialized and we are able to directly
# access frames from the camera to then display on the monitor for the user
# to see.


class Camera:

    def __init__(self):
        self.camera = PiCamera()
        res = (1920, 1088)
        self.camera.resolution = res
        self.camera.framerate = 120
        self.rawCapture = PiRGBArray(self.camera, size=res)

    def getFrame(self):
        # self.rawCapture.truncate(0)
        return self.camera.capture_continuous(
            self.rawCapture, format="bgr", use_video_port=True)
        # return self.rawCapture.array

    def reset(self):
        self.rawCapture.truncate(0)
