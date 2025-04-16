import cv2
import numpy as np
from json_cpp import JsonObject, JsonList

class Cameras(JsonList):
    def __init__(self):
        super().__init__(list_type=Camera)


class Camera(JsonObject):
    def __init__(self, name=str(), root=str(), roi=(224, 351, 10, 14)):
        self.name = name
        self.root = root
        self.fps = float()
        self.frame_count = int()
        self.width = int()
        self.height = int()
        self.roi = roi
        self.get_capture_properties()

    def select_roi(self):
        cap = cv2.VideoCapture(self.root)
        ret, frame = cap.read()
        print("Please select the ROI by dragging a box.")
        self.roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")  # Close the ROI selection window
        cap.release()

    def get_capture_properties(self):
        cap = cv2.VideoCapture(self.root)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT))
        cap.release()


def get_roi_intensity(filename, ROI=(224, 351, 10, 14)):
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    values = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        led = frame[ROI[1]:(ROI[1]+ROI[3]),ROI[0]:(ROI[0]+ROI[2]+1),1]
        values.append(np.mean(led))
    cap.release()
    return values, fps