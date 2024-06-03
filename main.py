import threading
import cv2
import numpy as np
from queue import Queue
from mediapipe_landmarks import MediaPipeLandmarks
from tracking_and_rotation import TrackingAndRotation
from rotation_gui import RotationGUI

def main():
    gui = RotationGUI()

    def update_rotation_callback(angle):
        gui.update_rotation(angle)

    tracker = TrackingAndRotation(update_rotation_callback)
    landmarks_processor = MediaPipeLandmarks()
    position_queue = Queue()

    def webcam_thread():
        while True:
            frame, results = landmarks_processor.process_frame()
            if results and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    tracker.update(hand_landmarks, landmarks_processor.width, landmarks_processor.height, position_queue)
                    landmarks_processor.drawing_utils.draw_landmarks(frame, hand_landmarks, landmarks_processor.mp_hands.HAND_CONNECTIONS)
            cv2.imshow('Webcam Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        landmarks_processor.release()
        cv2.destroyAllWindows()

    def compute_angle_worker():
        while True:
            if position_queue.qsize() >= 2:
                pos1 = position_queue.get()
                pos2 = position_queue.get()
                cx1, cy1 = pos1
                cx2, cy2 = pos2
                current_angle = tracker.compute_angle(cx2, cy2, cx1, cy1)
                if tracker.last_angle is not None:
                    angle_diff = np.degrees(current_angle - tracker.last_angle)
                    update_rotation_callback(angle_diff)
                tracker.last_angle = current_angle

    webcam_thread = threading.Thread(target=webcam_thread)
    worker_thread = threading.Thread(target=compute_angle_worker)

    webcam_thread.start()
    worker_thread.start()
    gui.run()

if __name__ == "__main__":
    main()
