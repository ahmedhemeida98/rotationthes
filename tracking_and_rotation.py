import numpy as np

class TrackingAndRotation:
    def __init__(self, update_rotation_callback, motion_threshold=20):
        self.motion_threshold = motion_threshold
        self.update_rotation_callback = update_rotation_callback
        self.initial_position = None
        self.tracking_started = False
        self.last_angle = None

    def compute_angle(self, cx, cy, origin_x, origin_y):
        return np.arctan2(cy - origin_y, cx - origin_x)

    def update(self, landmarks, width, height, position_queue):
        if landmarks:
            index_tip = landmarks.landmark[8]
            cx, cy = int(index_tip.x * width), int(index_tip.y * height)
            
            if self.initial_position is None:
                self.initial_position = (cx, cy)
            elif not self.tracking_started:
                initial_cx, initial_cy = self.initial_position
                distance = np.hypot(cx - initial_cx, cy - initial_cy)
                if distance > self.motion_threshold:
                    self.tracking_started = True
                    self.last_angle = None  # Reset last angle when tracking starts
            else:
                position_queue.put((cx, cy))
