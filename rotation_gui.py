import tkinter as tk
import math
from PIL import Image, ImageDraw, ImageTk

class RotationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rotatable Shape")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.angle = 0

        # Create an offscreen image for double buffering
        self.offscreen_image = Image.new("RGB", (500, 500), "white")
        self.offscreen_draw = ImageDraw.Draw(self.offscreen_image)
        self.tk_image = ImageTk.PhotoImage(self.offscreen_image)
        self.canvas_image_id = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        # Initial drawing on the offscreen buffer
        self.shape_coords = self.calculate_initial_coords()
        self.draw_rotated_shape()

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

    def draw_rotated_shape(self):
        # Clear the offscreen buffer
        self.offscreen_draw.rectangle([0, 0, 500, 500], fill="white")
        
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

        self.offscreen_draw.polygon(points, fill="blue")
        self.copy_buffer_to_canvas()

    def copy_buffer_to_canvas(self):
        # Update the offscreen image in the canvas
        self.tk_image.paste(self.offscreen_image)
        self.canvas.itemconfig(self.canvas_image_id, image=self.tk_image)

    def run(self):
        self.root.mainloop()
