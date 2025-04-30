# vision/face_auth.py
import face_recognition as fr
import cv2
import time
import os
import numpy as np

USER_DIR = "data/users"

def load_known_encodings():
    encodings = []
    for i in range(5):
        path = os.path.join(USER_DIR, f"AuthUser{i}.jpg")
        if os.path.exists(path):
            img = fr.load_image_file(path)
            encoding = fr.face_encodings(img)
            if encoding:
                encodings.append(encoding[0])
    return encodings

def save_new_user(self, frame):
    from datetime import datetime
    os.makedirs("data/users", exist_ok=True)
    for i in range(5):
        path = os.path.join("data/users", f"AuthUser{i}.jpg")
        if not os.path.exists(path):
            cv2.imwrite(path, frame)
            print(f"[AddUser] Saved {path}")
            # OPTIONAL: update in-memory encodings live
            img = fr.load_image_file(path)
            enc = fr.face_encodings(img)
            if enc:
                self.encodings.append(enc[0])
            return True
    print("[AddUser] Max user limit reached.")
    return False







class FaceAuthenticator:
    def __init__(self, shared, check_interval=1.0):
        self.shared = shared
        self.encodings = load_known_encodings()
        self.interval = check_interval

    def run(self):
        while True:
            frame = self.shared.get("frame")
            if frame is None:
                time.sleep(0.05)
                continue

            try:
                small = cv2.resize(frame, (320, 240))
                rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
                rgb = rgb.copy()


                # Save for visual debug
                cv2.imwrite("debug.jpg", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))

                # 🛡 Extra print-based type/shape check
                print(f"[FaceAuth DEBUG] dtype={rgb.dtype}, shape={rgb.shape}")
                if rgb is None:
                    print("[FaceAuth] rgb is None")
                    raise ValueError("rgb is None")
                if rgb.dtype != "uint8":
                    raise ValueError(f"Invalid dtype: {rgb.dtype}")
                if len(rgb.shape) != 3:
                    raise ValueError(f"Invalid shape (not 3D): {rgb.shape}")
                if rgb.shape[2] != 3:
                    raise ValueError(f"Invalid channel count: {rgb.shape[2]}")

                faces = fr.face_locations(rgb)
                encs = fr.face_encodings(rgb, faces)

                authorized = any(
                    any(fr.compare_faces(self.encodings, enc, tolerance=0.5)) for enc in encs
                )
                self.shared["authorized"] = authorized

            except Exception as e:
                print(f"[FaceAuth ERROR] {e}")
                self.shared["authorized"] = False

            time.sleep(self.interval)
