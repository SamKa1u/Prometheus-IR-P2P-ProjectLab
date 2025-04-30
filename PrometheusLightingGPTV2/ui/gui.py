# ui/gui.py
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class PrometheusApp:
    def __init__(self, root, shared_state, gesture_map, face_auth):
        self.root = root
        self.shared = shared_state
        self.gesture_map = gesture_map
        self.face_auth = face_auth

        self.root.title("Prometheus Lighting System")
        self.root.geometry("640x480")

        self.canvas = tk.Canvas(root, width=480, height=360)
        self.canvas.pack()

        self.label = tk.Label(root, text="Waiting for gesture...", font=("Arial", 14))
        self.label.pack(pady=10)

        self.auth_label = tk.Label(root, text="Status: Not Authenticated", font=("Arial", 12))
        self.auth_label.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.buttons = {}
        for gesture in ["red", "green", "blue", "bright", "dim"]:
            btn = tk.Button(self.button_frame, text=gesture.capitalize(), width=10)
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons[gesture] = btn

        self.add_user_button = tk.Button(root, text="Add User", command=self.add_user)
        self.add_user_button.pack(pady=5)

        self.last_gesture = None
        self.update()

    def update(self):
        frame = self.shared.get("frame")
        if frame is not None:
            frame = cv2.resize(frame, (480, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.img = img

        gesture = self.shared.get("gesture")
        if gesture:
            self.label.config(text=f"Detected gesture: {gesture}")
            if gesture != self.last_gesture:
                if gesture in self.buttons:
                    self.buttons[gesture].config(bg="lightgreen")
                    self.root.after(300, lambda: self.buttons[gesture].config(bg="SystemButtonFace"))
                self.last_gesture = gesture
        else:
            self.label.config(text="Waiting for gesture...")

        authorized = self.shared.get("authorized")
        if authorized:
            self.auth_label.config(text="Status: ✅ Authorized", fg="green")
        else:
            self.auth_label.config(text="Status: ❌ Not Authorized", fg="red")

        self.root.after(30, self.update)

    def add_user(self):
        frame = self.shared.get("frame")
        if frame is not None:
            success = self.face_auth.save_new_user(frame)
            if success:
                print("✅ New user saved.")
            else:
                print("❌ Could not save new user.")
