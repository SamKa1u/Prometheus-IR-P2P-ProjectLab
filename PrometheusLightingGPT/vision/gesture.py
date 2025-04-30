# vision/gesture.py
import time
from ultralytics import YOLO
from config import GESTURE_MAP

class GestureDetector:
    def __init__(self, shared, model_path):
        self.shared = shared
        self.model = YOLO(model_path)

    def run(self):
        while True:
            frame = self.shared.get("frame")
            if frame is None:
                time.sleep(0.01)
                continue

            results = self.model.predict(frame, conf=0.65, imgsz=480, max_det=1, verbose=False)
            for result in results:
                boxes = result.boxes.cls.tolist()
                if boxes:
                    label = int(boxes[0])
                    gesture = GESTURE_MAP.get(label, None)
                    if gesture:
                        print(f"Detected gesture: {gesture}")
                        self.shared["gesture"] = gesture
            time.sleep(0.5)
