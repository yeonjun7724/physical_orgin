import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame):
        """프레임에서 pose landmarks 추출"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)
        if result.pose_landmarks:
            return result.pose_landmarks.landmark
        return None
