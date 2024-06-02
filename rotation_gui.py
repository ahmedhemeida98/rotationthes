import tkinter as tk
import math
import threading
from mediapipe_landmarks import MediaPipeLandmarks
from tracking_and_rotation import TrackingAndRotation

class RotationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rotatable Shape")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.shape = self.canvas.create_polygon(self.calculate_initial_coords(), fill="blue")
        self.angle = 0

        self.start_webcam_button = tk.Button(self.root, text="Start Webcam", command=self.start_webcam)
        self.start_webcam_button.pack()

    def calculate_initial_coords(self):
        cx, cy = 250, 250
        w, h = 100, 150
        points = [
            (cx + w / 2, cy + h / 2),
            (cx, cy + h / 2 + 50),
            (cx - w / 2, cy + h / 2),
            (cx - w / 2, cy - h / 2),
            (cx + w / 2, cy - h / 2)
        ]
        return points

    def update_rotation(self, angle):
        self.angle += angle
        self.draw_rotated_shape()

    def reset_rotation(self):
        self.angle = 0
        self.draw_rotated_shape()

    def draw_rotated_shape(self):
        cx, cy = 250, 250
        w, h = 100, 150
        angle_rad = math.radians(self.angle)
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        points = [
            (cx + w / 2 * cos_val - h / 2 * sin_val, cy + w / 2 * sin_val + h / 2 * cos_val),
            (cx + 0 * cos_val - (h / 2 + 50) * sin_val, cy + 0 * sin_val + (h / 2 + 50) * cos_val),
            (cx - w / 2 * cos_val - h / 2 * sin_val, cy - w / 2 * sin_val + h / 2 * cos_val),
            (cx - w / 2 * cos_val + h / 2 * sin_val, cy - w / 2 * sin_val - h / 2 * cos_val),
            (cx + w / 2 * cos_val + h / 2 * sin_val, cy + w / 2 * sin_val - h / 2 * cos_val)
        ]
        self.canvas.coords(self.shape, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1], points[4][0], points[4][1])

    def start_webcam(self):
        self.detector = HandMotionDetector(self.update_rotation)
        self.detector_thread = threading.Thread(target=self.detector.run)
        self.detector_thread.start()

    def run(self):
        self.root.mainloop()