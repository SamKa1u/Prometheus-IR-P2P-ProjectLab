# main.py — GUI with camera and gesture detection hook

import tkinter as tk
from ui.gui import PrometheusApp
from vision.camera import CameraStream
from vision.gesture import GestureDetector
from config import MODEL_PATH, GESTURE_MAP

import threading

shared_state = {
    "frame": None,
    "gesture": None,
}

# --- Start Camera Thread ---
camera = CameraStream(shared_state)
camera_thread = threading.Thread(target=camera.run, daemon=True)
camera_thread.start()

# --- Start Gesture Detection Thread ---
gesture_detector = GestureDetector(shared_state, model_path=MODEL_PATH)
gesture_thread = threading.Thread(target=gesture_detector.run, daemon=True)
gesture_thread.start()

# --- Launch GUI ---
root = tk.Tk()
app = PrometheusApp(root, shared_state, gesture_map=GESTURE_MAP)
root.mainloop()
