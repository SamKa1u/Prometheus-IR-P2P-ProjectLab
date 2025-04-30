# vision/camera.py
import cv2
import time

class CameraStream:
    def __init__(self, shared):
        self.shared = shared
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.shared["frame"] = frame
            time.sleep(0.01)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
