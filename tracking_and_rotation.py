import numpy as np
import math
from scipy.optimize import leastsq
import time

class TrackingAndRotation:
    def __init__(self, update_rotation_callback, motion_threshold=20, interval=0.2):
        self.motion_threshold = motion_threshold
        self.interval = interval
        self.positions = []
        self.timestamps = []
        self.path = []
        self.tracking = False
        self.last_angle = None
        self.total_rotation = 0
        self.update_rotation_callback = update_rotation_callback
        self.movements_log = []

    def append_values(self, cx, cy, current_time):
        self.positions.append((cx, cy))
        self.timestamps.append(current_time)
        self.movements_log.append((current_time, (cx, cy)))

        while self.timestamps and current_time - self.timestamps[0] > self.interval:
            self.positions.pop(0)
            self.timestamps.pop(0)

    def compute_distance(self):
        step_distances = []
        for i in range(1, len(self.positions)):
            previous_pos = self.positions[i - 1]
            current_pos = self.positions[i]
            step_distance = math.sqrt((current_pos[0] - previous_pos[0])**2 + (current_pos[1] - previous_pos[1])**2)
            step_distances.append(step_distance)
        return sum(step_distances)

    def fit_circle(self, x, y):
        if len(x) < 3 or len(y) < 3:
            raise ValueError("At least 3 points are required to fit a circle")

        def calc_R(xc, yc):
            return np.sqrt((x - xc)**2 + (y - yc)**2)

        def f_2(c):
            Ri = calc_R(*c)
            return Ri - Ri.mean()

        center_estimate = np.mean(x), np.mean(y)
        center, ier = leastsq(f_2, center_estimate)
        xc, yc = center
        Ri = calc_R(xc, yc)
        R = Ri.mean()
        return xc, yc, R

    def compute_angles(self, cx, cy):
        angles = [np.arctan2(y - cy, x - cx) for x, y in self.path]
        return angles

    def compute_rotation(self, angles):
        total_rotation = 0
        for i in range(1, len(angles)):
            delta_angle = angles[i] - angles[i - 1]
            if delta_angle > np.pi:
                delta_angle -= 2 * np.pi
            elif delta_angle < -np.pi:
                delta_angle += 2 * np.pi
            total_rotation += delta_angle
        return total_rotation

    def start_tracking(self):
        self.tracking = True
        self.path = []
        self.total_rotation = 0
        self.last_angle = None

    def stop_tracking(self):
        self.tracking = False
        if len(self.path) < 3:
            print("Not enough points to fit a circle")
            return

        if self.path:
            x = np.array([p[0] for p in self.path])
            y = np.array([p[1] for p in self.path])
            try:
                cx, cy, r = self.fit_circle(x, y)
                angles = self.compute_angles(cx, cy)
                total_rotation = self.compute_rotation(angles)

                print(f"Circle center: ({cx}, {cy}), Radius: {r}")
                print(f"Total Rotation: {np.degrees(total_rotation):.2f} degrees")

                path_length = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
                circumference = 2 * np.pi * r
                if path_length >= circumference:
                    circle_type = "Complete Circle"
                else:
                    circle_type = "Part of a Circle"

                print(f"Path Type: {circle_type}")

                self.circle_center = (int(cx), int(cy))
                self.circle_radius = int(r)
                self.total_rotation = np.degrees(total_rotation)
                self.circle_type = circle_type

                self.update_rotation_callback(self.total_rotation)
            except ValueError as e:
                print(f"Error fitting circle: {e}")

    def delete_path(self):
        self.path = []

    def append_to_path(self, cx, cy):
        if self.tracking:
            self.path.append((cx, cy))

    def visualize_path(self, frame):
        for i in range(1, len(self.path)):
            cv2.line(frame, self.path[i - 1], self.path[i], (0, 255, 0), 2)

    def update(self, landmarks, width, height):
        index_tip = landmarks.landmark[8]
        cx, cy = int(index_tip.x * width), int(index_tip.y * height)

        self.append_values(cx, cy, time.time())
        self.append_to_path(cx, cy)

        total_distance = self.compute_distance()

        if total_distance > self.motion_threshold:
            if not self.tracking:
                self.start_tracking()
        else:
            if self.tracking:
                self.stop_tracking()