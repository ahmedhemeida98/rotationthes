import threading
import cv2
from mediapipe_landmarks import MediaPipeLandmarks
from tracking_and_rotation import TrackingAndRotation
from rotation_gui import RotationGUI

def main():
    gui = RotationGUI()

    def update_rotation_callback(angle):
        gui.update_rotation(angle)

    tracker = TrackingAndRotation(update_rotation_callback)
    landmarks_processor = MediaPipeLandmarks()

    def webcam_thread():
        while True:
            frame, results = landmarks_processor.process_frame()
            if results and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    tracker.update(hand_landmarks, landmarks_processor.width, landmarks_processor.height)
                    landmarks_processor.drawing_utils.draw_landmarks(frame, hand_landmarks, landmarks_processor.mp_hands.HAND_CONNECTIONS)
            cv2.imshow('Webcam Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        landmarks_processor.release()
        cv2.destroyAllWindows()

    thread = threading.Thread(target=webcam_thread)
    thread.start()
    gui.run()

if __name__ == "__main__":
    main()
