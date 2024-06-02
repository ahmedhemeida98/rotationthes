import numpy as np

class TrackingAndRotation:
    def __init__(self, update_rotation_callback, motion_threshold=20):
        self.motion_threshold = motion_threshold
        self.update_rotation_callback = update_rotation_callback
        self.origin_x = None
        self.origin_y = None
        self.last_angle = None

    def compute_angle(self, cx, cy):
        if self.origin_x is None or self.origin_y is None:
            self.origin_x, self.origin_y = cx, cy
        return np.arctan2(cy - self.origin_y, cx - self.origin_x)

    def update(self, landmarks, width, height):
        if landmarks:
            index_tip = landmarks.landmark[8]
            cx, cy = int(index_tip.x * width), int(index_tip.y * height)
            current_angle = self.compute_angle(cx, cy)
            if self.last_angle is not None:
                angle_diff = np.degrees(current_angle - self.last_angle)
                self.update_rotation_callback(angle_diff)
            self.last_angle = current_angle
