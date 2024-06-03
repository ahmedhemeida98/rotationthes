import numpy as np

class TrackingAndRotation:
    def __init__(self, update_rotation_callback, motion_threshold=20):
        self.motion_threshold = motion_threshold
        self.update_rotation_callback = update_rotation_callback
        self.origin_x = None
        self.origin_y = None
        self.last_angle = None

    def compute_angle(self, cx, cy, origin_x, origin_y):
        return np.arctan2(cy - origin_y, cx - origin_x)

    def update(self, landmarks, width, height, position_queue):
        if landmarks:
            index_tip = landmarks.landmark[8]
            cx, cy = int(index_tip.x * width), int(index_tip.y * height)
            position_queue.put((cx, cy))
