# ======================================================================
# 0. 색상 / 테마 관련 상수
# ======================================================================

COLORS = {
    "MAIN_BLUE": "#4c84af",
    "ACCENT_BLUE": "#81bfc7",
    "LIGHT_BLUE": "#e3f2fd",
    "MEDIUM_BLUE": "#64b5f6",
    "DARK_BLUE": "#1976d2",
    "BLUE_BG": "#f0f7fa",
    "TEXT_DARK": "#222",
    "TEXT_LIGHT": "#fafafa",
    "TEXT_GRAY": "#666",
    "TEXT_LIGHT_GRAY": "#999",
    "BG_LIGHT": "#f9f9f9",
    "BG_WHITE": "#ffffff",
    "BORDER_LIGHT": "#eee",
}


# ======================================================================
# 1. 사용자 기본 정보 관련 상수 (나이/지역/종목)
# ======================================================================

AGE_GROUPS = {
    "유아기": [4, 6],  # 48개월~83개월 (만 4세~만 6세 11개월)
    "유소년기": [11, 12],  # 만 11세~12세
    "청소년기": [13, 18],  # 만 13세~18세
    "성인기": [19, 64],  # 만 19세~64세
    "어르신기": [65, 100]  # 만 65세 이상
}


REGIONS = [
    "서울", "경기", "인천", "부산", "대구", "광주",
    "대전", "울산", "강원", "충북", "충남",
    "전북", "전남", "경북", "경남", "제주"
]

# 내부 key 통일: pushup, situp, squat, balance, knee_lift, trunk_flex
EVENTS = [
    "pushup",
    "situp",
    "squat",
    "balance",
    "knee_lift",
    "trunk_flex"
]


# ======================================================================
# 2. 포인트 규칙 & 기본 포인트 데이터
# ======================================================================

POINT_RULES = {
    "measurement_completed": 10,      # 측정 완료
    "grade_improved": 30,             # 등급 상승
    "daily_login": 5,                 # 일일 로그인
    "streak_bonus": 10,               # 스트릭 유지 보너스
}

DEFAULT_USER_POINTS = {
    "total_points": 0,
    "earned_points": 0,
    "spent_points": 0,
    "last_updated": None
}


# ======================================================================
# 3. Daily Streak 규칙 & 템플릿
# ======================================================================

STREAK_RULES = {
    "max_gap_hours": 36,              # 하루 + 12시간 여유
    "reward_points": 10,              # 연속 운동 보상 포인트
    "milestones": [3, 7, 14, 30]      # 특정 일수 달성 시 뱃지 혹은 보너스
}

DEFAULT_DAILY_STREAK = {
    "current_streak": 0,
    "longest_streak": 0,
    "last_measurement_date": None,
    "streak_start_date": None,
    "updated_at": None
}


# ======================================================================
# 4. 뱃지(Badge) 관련 상수
# ======================================================================

BADGE_MASTER = {
    1: {
        "badge_id": 1,
        "name": "첫 측정",
        "description": "첫번째 종목 측정을 완료했습니다!",
        "icon": "badge_first.png"
    },
    2: {
        "badge_id": 2,
        "name": "3일 연속",
        "description": "3일 연속으로 운동을 기록했습니다.",
        "icon": "badge_streak3.png"
    },
    3: {
        "badge_id": 3,
        "name": "10점 향상",
        "description": "이전 기록 대비 점수가 향상되었습니다!",
        "icon": "badge_improve10.png"
    },
    4: {
        "badge_id": 4,
        "name": "철인",
        "description": "6개 모든 종목을 도전했습니다!",
        "icon": "badge_all_events.png"
    }
}

