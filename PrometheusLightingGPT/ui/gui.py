# ui/gui.py
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class PrometheusApp:
    def __init__(self, root, shared_state, gesture_map):
        self.root = root
        self.shared = shared_state
        self.gesture_map = gesture_map

        self.root.title("Prometheus Lighting System")
        self.root.geometry("640x480")

        self.canvas = tk.Canvas(root, width=480, height=360)
        self.canvas.pack()

        self.label = tk.Label(root, text="Waiting for gesture...", font=("Arial", 14))
        self.label.pack(pady=10)

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
        if gesture:
            self.label.config(text=f"Detected gesture: {gesture}")
            if gesture in self.buttons:
                self.buttons[gesture].config(bg="lightgreen")
                self.root.after(300, lambda: self.buttons[gesture].config(bg="SystemButtonFace"))
        else:
            self.label.config(text="Waiting for gesture...")

        self.root.after(30, self.update)
