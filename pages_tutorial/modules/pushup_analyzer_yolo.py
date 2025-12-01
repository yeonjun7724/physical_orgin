# modules/pushup_analyzer_yolo.py
import math
import numpy as np


def safe_age_to_int(age):
    """나이값 문자열(예: '20-24') 등을 안전하게 정수로 변환"""
    if isinstance(age, int) or isinstance(age, float):
        return int(age)

    if isinstance(age, str):
        age = age.strip()

        # "20-24" 같은 구간이면 중앙값 반환
        if "-" in age:
            try:
                a, b = age.split("-")
                return (int(a) + int(b)) // 2
            except:
                pass

        # "23" 같은 값
        try:
            return int(age)
        except:
            pass

    # 실패하면 기본값 25
    return 25



class PushupAnalyzerYolo:
    def __init__(self):
        self.prev_position = None  # "up" / "down"
        self.pushup_count = 0
        self.quality_scores = []

    @staticmethod
    def angle_3pts(a, b, c):
        """세 점(a,b,c)의 각도 계산"""
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
        """YOLO keypoints로 1프레임 분석"""
        if keypoints is None:
            return

        try:
            shoulder = keypoints[6]
            elbow = keypoints[8]
            wrist = keypoints[10]
        except IndexError:
            return

        # 신뢰도 낮으면 skip
        if shoulder[2] < 0.3 or elbow[2] < 0.3 or wrist[2] < 0.3:
            return

        elbow_angle = self.angle_3pts(shoulder, elbow, wrist)

        # Down / Up 기준
        if elbow_angle < 70:
            current_position = "down"
        elif elbow_angle > 150:
            current_position = "up"
        else:
            current_position = self.prev_position

        # down → up 시 카운트
        if self.prev_position == "down" and current_position == "up":
            self.pushup_count += 1

        # 품질 점수 (90도 기준)
        quality = max(0, 100 - abs(90 - elbow_angle))
        self.quality_scores.append(quality)

        self.prev_position = current_position

    def avg_quality_score(self):
        if not self.quality_scores:
            return 0
        return round(float(np.mean(self.quality_scores)), 1)

    def calculate_kspo_grade(self, count, age, gender):
        """
        국민체력100 팔굽혀펴기 기준(축약판)으로 등급 계산
        """

        # 🔥 age를 항상 정수로 변환 (에러 방지)
        age = safe_age_to_int(age)

        # 나이대 분류
        if age < 30:
            age_group = "20대"
        elif age < 40:
            age_group = "30대"
        else:
            age_group = "40대"

        # 기준치 테이블
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

        if gender == "남":
            base = table_male
        else:
            base = table_female

        # age_group이 테이블에 없으면 fallback
        thresholds = base.get(age_group, base["40대"])

        # 등급 판정
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
