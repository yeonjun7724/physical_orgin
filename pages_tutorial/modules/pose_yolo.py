# modules/pose_yolo.py
from ultralytics import YOLO
import numpy as np

class YoloPoseDetector:
    def __init__(self, model_name: str = "yolov8n-pose.pt"):
        """
        YOLOv8 pose 모델 로드
        - model_name은 기본으로 ultralytics에서 제공하는 경량 pose 모델 사용
        """
        self.model = YOLO(model_name)

    def detect_keypoints(self, frame):
        """
        입력: BGR 이미지 (OpenCV 프레임)
        출력: keypoints (numpy 배열) 또는 None
          - shape: (num_keypoints, 3)  → [x, y, confidence]
        """
        results = self.model(frame, verbose=False)
        if len(results) == 0:
            return None

        kp = results[0].keypoints
        if kp is None or kp.data is None:
            return None

        # (1, num_kpts, 3) → (num_kpts, 3)
        keypoints = kp.data[0].cpu().numpy()
        return keypoints

    @staticmethod
    def get_kpt(keypoints, idx):
        """
        편의를 위한 키포인트 인덱싱 함수
        idx: COCO keypoint index (0~16)
        """
        if keypoints is None:
            return None
        if idx < 0 or idx >= keypoints.shape[0]:
            return None
        return keypoints[idx]
