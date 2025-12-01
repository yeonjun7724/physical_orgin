# modules/pushup_analyzer_yolo.py
import math
import numpy as np

class PushupAnalyzerYolo:
    def __init__(self):
        self.prev_position = None  # "up" / "down"
        self.pushup_count = 0
        self.quality_scores = []

    @staticmethod
    def angle_3pts(a, b, c):
        """
        세 점 (a, b, c)의 각도 계산
        a, b, c: [x, y, conf]
        """
        ax, ay = a[0], a[1]
        bx, by = b[0], b[1]
        cx, cy = c[0], c[1]

        ang = math.degrees(
            math.atan2(cy - by, cx - bx) - math.atan2(ax - bx, ay - by)
        )
        ang = abs(ang)
        if ang > 180:
            ang = 360 - ang
        return ang

    def process_frame(self, keypoints):
        """
        한 프레임의 keypoints를 받아 팔꿈치 각도를 기반으로 팔굽혀펴기 상태/횟수 업데이트
        COCO keypoint index 기준:
          6: 오른쪽 어깨 (right_shoulder)
          8: 오른쪽 팔꿈치 (right_elbow)
          10: 오른쪽 손목 (right_wrist)
        """
        if keypoints is None:
            return

        try:
            shoulder = keypoints[6]  # right_shoulder
            elbow = keypoints[8]     # right_elbow
            wrist = keypoints[10]    # right_wrist
        except IndexError:
            return

        # confidence 체크 (너무 낮으면 skip)
        if shoulder[2] < 0.3 or elbow[2] < 0.3 or wrist[2] < 0.3:
            return

        elbow_angle = self.angle_3pts(shoulder, elbow, wrist)

        # Down / Up 기준 (예시 값, 나중에 튜닝 가능)
        # - 내려갈 때: 팔꿈치 각도가 70도 이하
        # - 올라왔을 때: 팔꿈치 각도가 150도 이상
        if elbow_angle < 70:
            current_position = "down"
        elif elbow_angle > 150:
            current_position = "up"
        else:
            current_position = self.prev_position

        # down → up 변화할 때 1회 카운트
        if self.prev_position == "down" and current_position == "up":
            self.pushup_count += 1

        # 품질 점수: 90도 근처에서 얼마나 잘 내려갔는지 기준
        quality = max(0, 100 - abs(90 - elbow_angle))
        self.quality_scores.append(quality)

        self.prev_position = current_position

    def avg_quality_score(self):
        if not self.quality_scores:
            return 0
        return round(float(np.mean(self.quality_scores)), 1)

    def calculate_kspo_grade(self, count, age, gender):
        """
        국민체력100 팔굽혀펴기 기준을 단순화해서 등급화.
        - 실제 KSPO 표를 그대로 가져와도 되지만, 여기서는 예시용 로직.
        """
        # 단순 그룹화
        if age < 30:
            age_group = "20대"
        elif age < 40:
            age_group = "30대"
        else:
            age_group = "40대"

        # 예시 기준 (필요하면 실제 표로 교체)
        table_male = {
            "20대": [45, 40, 35, 30],
            "30대": [40, 35, 30, 25],
            "40대": [35, 30, 25, 20],
        }

        table_female = {
            "20대": [30, 25, 20, 15],
            "30대": [28, 23, 18, 13],
            "40대": [25, 20, 15, 10],
        }

        base = table_male if gender == "남" else table_female

        if age_group not in base:
            # 범위 밖이면 가장 낮은 기준 사용
            thresholds = base["40대"]
        else:
            thresholds = base[age_group]

        if count >= thresholds[0]:
            return "1등급"
        elif count >= thresholds[1]:
            return "2등급"
        elif count >= thresholds[2]:
            return "3등급"
        elif count >= thresholds[3]:
            return "4등급"
        else:
            return "5등급"
