# ui/gui.py
import cv2
import tkinter as tk
from PIL import Image, ImageTk



class PrometheusApp:
    def __init__(self, root, shared_state, gesture_map):
        self.icon = Image.open("ui/prometheus_icon.png")
        self.icon_photo = ImageTk.PhotoImage(self.icon)
        self.root = root
        self.root.iconphoto(False, self.icon_photo)
        self.shared = shared_state
        self.gesture_map = gesture_map

        self.root.title("Prometheus Lighting System")
        self.root.geometry("640x480")

        self.canvas = tk.Canvas(root, width=480, height=360)
        self.canvas.pack()

        self.label = tk.Label(root, text="Waiting for gesture...", font=("Arial", 14))
        self.label.pack(pady=5)

        self.auth_label = tk.Label(root, text="Status: Not Authenticated", font=("Arial", 12))
        self.auth_label.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.buttons = {}
        for gesture in ["red", "green", "blue", "bright", "dim"]:
            btn = tk.Button(self.button_frame, text=gesture.capitalize(), width=10)
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons[gesture] = btn

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
        #if authenticated display authorized
        if self.shared.get("authenticated") is True:
            self.auth_label.config(text="Status: ✅ Authorized", fg="green")
            #if authenticated and gesture detected display gesture
            if gesture:
                self.label.config(text=f"Detected gesture: {gesture}")
                #if gesture is a button indicate with color change
                if gesture in self.buttons:
                    self.buttons[gesture].config(bg="lightgreen")
                    self.root.after(300, lambda: self.buttons[gesture].config(bg="SystemButtonFace"))

            #wait if no gesture detected
            else:
                self.label.config(text="Waiting for gesture...")
        #if not authenticated inform user gesture control is off
        else:
            self.auth_label.config(text="Status: ❌ Not Authorized", fg="red")
            self.label.config(text="Gesture Control Off")

        self.root.after(30, self.update)
