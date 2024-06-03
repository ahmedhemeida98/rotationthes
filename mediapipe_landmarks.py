import cv2
import mediapipe as mp

class MediaPipeLandmarks:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        frame = cv2.flip(frame, 1)
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return frame, results

    def release(self):
        self.cap.release()
        self.hands.close()
