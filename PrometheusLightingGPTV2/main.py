# main.py — GUI with camera and gesture detection hook

import tkinter as tk
from ui.gui import PrometheusApp
from vision.camera import CameraStream
from vision.gesture import GestureDetector
from config import MODEL_PATH, GESTURE_MAP
from vision.face_auth import FaceAuthenticator
import threading
#from utils.pwm_output import cleanup not working, requies intilizing stuff on pi, will work on pi though


shared_state = {
    "frame": None,
    "gesture": None,
    "authorized": False
}

# --- Start Camera Thread ---
camera = CameraStream(shared_state)
camera_thread = threading.Thread(target=camera.run, daemon=True)
camera_thread.start()

# Add this after camera thread:
face_auth = FaceAuthenticator(shared_state)
face_thread = threading.Thread(target=face_auth.run, daemon=True)
face_thread.start()

# --- Start Gesture Detection Thread ---
gesture_detector = GestureDetector(shared_state, model_path=MODEL_PATH)
gesture_thread = threading.Thread(target=gesture_detector.run, daemon=True)
gesture_thread.start()

# --- Launch GUI ---
root = tk.Tk()
app = PrometheusApp(root, shared_state, gesture_map=GESTURE_MAP, face_auth=face_auth)
#try:
root.mainloop()
#finally:
    #cleanup()