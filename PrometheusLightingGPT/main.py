# main.py — GUI with camera and gesture detection hook

import tkinter as tk
from ui.gui import PrometheusApp
from vision.camera import CameraStream
from vision.gesture import GestureDetector
from FlaskAddUser.AddUser import FileServer
from Auth.facialAuthenticator import Authenticator
from config import MODEL_PATH, AUTH_USER_PATH, GESTURE_MAP, FLASK

import threading

shared_state = {
    "frame": None,
    "gesture": None,
    "encodingBools": [False,False,False,False,False],
    "authenticated" : False,
}

# --- Start Camera Thread ---
camera = CameraStream(shared_state)
camera_thread = threading.Thread(target=camera.run, daemon=True)
camera_thread.start()

# --- Start Gesture Detection Thread ---
gesture_detector = GestureDetector(shared_state, model_path=MODEL_PATH)
gesture_thread = threading.Thread(target=gesture_detector.run, daemon=True)
gesture_thread.start()

# --- Start Facial Recognition Thread ---
facial_authenticator = Authenticator(shared_state, auth_path=AUTH_USER_PATH)
auth_thread = threading.Thread(target=facial_authenticator.processing, daemon=True)
auth_thread.start()

# --- Start Flask AddUser Thread ---
flask_server = FileServer(bind_host=FLASK[0], auth_username=FLASK[1], auth_passkey=FLASK[2])
flask_server.daemon = True
flask_server.start()

# --- Launch GUI ---
root = tk.Tk()
app = PrometheusApp(root, shared_state, gesture_map=GESTURE_MAP)
root.mainloop()
