import mediapipe as mp
import math

class PushupAnalyzer:
    def __init__(self):
        self.prev_position = None
        self.pushup_count = 0
        self.positions = []
        self.quality_scores = []

    # -----------------------------
    # 보조 함수: 세 점으로 각도 계산
    # -----------------------------
    def angle(self, a, b, c):
        ang = math.degrees(
            math.atan2(c.y - b.y, c.x - b.x) - 
            math.atan2(a.y - b.y, a.x - b.x)
        )
        return abs(ang)

    # -----------------------------
    # 프레임 처리
    # -----------------------------
    def process_frame(self, lm):
        if lm is None:
            return

        # 팔꿈치 각도 계산 (오른팔 기준)
        shoulder = lm[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        elbow = lm[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]
        wrist = lm[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]

        angle_elbow = self.angle(shoulder, elbow, wrist)

        # Up / Down 판정
        position = "down" if angle_elbow < 70 else "up"

        # Up → Down → Up 시 횟수 증가
        if self.prev_position == "down" and position == "up":
            self.pushup_count += 1

        # 자세 품질 점수 (0~100)
        quality_score = max(0, 100 - abs(90 - angle_elbow))
        self.quality_scores.append(quality_score)

        self.prev_position = position

    def avg_quality_score(self):
        if len(self.quality_scores) == 0:
            return 0
        return round(sum(self.quality_scores) / len(self.quality_scores), 1)

    # ----------------------------------------------------
    # 국민체력100 기준 적용 (남/여, 연령대 비교 점수)
    # ----------------------------------------------------
    def calculate_kspo_grade(self, count, age, gender):
        """
        국민체력100 기준 근지구력(팔굽혀펴기)을 기반으로 등급 부여
        """

        # 간단화된 기준 (정확한 KSPO 표 그대로 매핑 가능)
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

        if age < 30:
            age_group = "20대"
        elif age < 40:
            age_group = "30대"
        else:
            age_group = "40대"

        base = table_male[age_group] if gender == "남" else table_female[age_group]

        if count >= base[0]:
            return "1등급"
        elif count >= base[1]:
            return "2등급"
        elif count >= base[2]:
            return "3등급"
        elif count >= base[3]:
            return "4등급"
        else:
            return "5등급"
