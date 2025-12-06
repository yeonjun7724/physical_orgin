from data.constants import AGE_GROUPS
from data.constants import COLORS

# ======================================================================
# 5. 리더보드 관련 상수
# ======================================================================

LEADERBOARD_BUCKETS = {
    "age_groups": list(AGE_GROUPS.keys()),
    "genders": ["male", "female"],
    "periods": ["weekly", "monthly", "season"]
}

LEADERBOARD_SAMPLE = {
# ---------------------------------------------------
# OVERALL (종합 리더보드)
# ---------------------------------------------------
    "overall": {

        "weekly": [
            {"user_id": "ov001", "nickname": "철수", "score": 510, "rank": 1},
            {"user_id": "ov002", "nickname": "영희", "score": 492, "rank": 2},
            {"user_id": "ov003", "nickname": "산들", "score": 480, "rank": 3},
            {"user_id": "ov004", "nickname": "지훈", "score": 468, "rank": 4},
            {"user_id": "ov005", "nickname": "서연", "score": 455, "rank": 5},
            {"user_id": "ov006", "nickname": "준호", "score": 447, "rank": 6},
            {"user_id": "ov007", "nickname": "지아", "score": 440, "rank": 7},
            {"user_id": "ov008", "nickname": "유진", "score": 432, "rank": 8},
            {"user_id": "ov009", "nickname": "현아", "score": 421, "rank": 9},
            {"user_id": "ov010", "nickname": "도현", "score": 415, "rank": 10},
        ],

        "monthly": [
            {"user_id": "ov011", "nickname": "태호", "score": 540, "rank": 1},
            {"user_id": "ov002", "nickname": "영희", "score": 525, "rank": 2},
            {"user_id": "ov012", "nickname": "다현", "score": 508, "rank": 3},
            {"user_id": "ov013", "nickname": "정민", "score": 501, "rank": 4},
            {"user_id": "ov014", "nickname": "가윤", "score": 495, "rank": 5},
            {"user_id": "ov015", "nickname": "하린", "score": 489, "rank": 6},
            {"user_id": "ov016", "nickname": "산들", "score": 480, "rank": 7},
            {"user_id": "ov017", "nickname": "예린", "score": 472, "rank": 8},
            {"user_id": "ov018", "nickname": "도윤", "score": 466, "rank": 9},
            {"user_id": "ov019", "nickname": "라온", "score": 459, "rank": 10},
        ],

        "season": [
            {"user_id": "ov020", "nickname": "태호", "score": 560, "rank": 1},
            {"user_id": "ov021", "nickname": "영희", "score": 542, "rank": 2},
            {"user_id": "ov022", "nickname": "철수", "score": 530, "rank": 3},
            {"user_id": "ov023", "nickname": "도하", "score": 520, "rank": 4},
            {"user_id": "ov024", "nickname": "하준", "score": 516, "rank": 5},
            {"user_id": "ov025", "nickname": "수민", "score": 510, "rank": 6},
            {"user_id": "ov026", "nickname": "예진", "score": 502, "rank": 7},
            {"user_id": "ov027", "nickname": "채윤", "score": 495, "rank": 8},
            {"user_id": "ov028", "nickname": "민재", "score": 488, "rank": 9},
            {"user_id": "ov029", "nickname": "지우", "score": 482, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # PUSHUP (팔굽혀펴기)
    # ---------------------------------------------------
    "pushup": {
        "weekly": [
            {"user_id": "u001", "nickname": "철수", "score": 85, "rank": 1},
            {"user_id": "u002", "nickname": "영희", "score": 82, "rank": 2},
            {"user_id": "u003", "nickname": "민수", "score": 79, "rank": 3},
            {"user_id": "u004", "nickname": "지연", "score": 77, "rank": 4},
            {"user_id": "u005", "nickname": "준호", "score": 75, "rank": 5},
            {"user_id": "u006", "nickname": "산들들", "score": 73, "rank": 6},
            {"user_id": "u007", "nickname": "서연", "score": 72, "rank": 7},
            {"user_id": "u008", "nickname": "지훈", "score": 70, "rank": 8},
            {"user_id": "u009", "nickname": "유진", "score": 68, "rank": 9},
            {"user_id": "u010", "nickname": "지수", "score": 67, "rank": 10},
        ],
        "monthly": [
            {"user_id": "u011", "nickname": "태호", "score": 95, "rank": 1},
            {"user_id": "u002", "nickname": "산들", "score": 92, "rank": 2},
            {"user_id": "u005", "nickname": "준호", "score": 89, "rank": 3},
            {"user_id": "u012", "nickname": "다현", "score": 87, "rank": 4},
            {"user_id": "u013", "nickname": "정민", "score": 85, "rank": 5},
            {"user_id": "u014", "nickname": "가윤", "score": 82, "rank": 6},
            {"user_id": "u015", "nickname": "라온", "score": 80, "rank": 7},
            {"user_id": "u016", "nickname": "민재", "score": 78, "rank": 8},
            {"user_id": "u017", "nickname": "예린", "score": 76, "rank": 9},
            {"user_id": "u018", "nickname": "도윤", "score": 74, "rank": 10},
        ],
        "season": [
            {"user_id": "u020", "nickname": "서연", "score": 102, "rank": 1},
            {"user_id": "u021", "nickname": "지환", "score": 99, "rank": 2},
            {"user_id": "u022", "nickname": "지민", "score": 96, "rank": 3},
            {"user_id": "u023", "nickname": "지유", "score": 94, "rank": 4},
            {"user_id": "u024", "nickname": "하준", "score": 92, "rank": 5},
            {"user_id": "u025", "nickname": "수민", "score": 90, "rank": 6},
            {"user_id": "u026", "nickname": "예진", "score": 89, "rank": 7},
            {"user_id": "u027", "nickname": "채윤", "score": 87, "rank": 8},
            {"user_id": "u028", "nickname": "산들들", "score": 85, "rank": 9},
            {"user_id": "u029", "nickname": "시후", "score": 83, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # SITUP (윗몸일으키기)
    # ---------------------------------------------------
    "situp": {
        "weekly": [
            {"user_id": "su001", "nickname": "지훈", "score": 62, "rank": 1},
            {"user_id": "su002", "nickname": "세영", "score": 60, "rank": 2},
            {"user_id": "su003", "nickname": "산들들", "score": 58, "rank": 3},
            {"user_id": "su004", "nickname": "지안", "score": 56, "rank": 4},
            {"user_id": "su005", "nickname": "채민", "score": 54, "rank": 5},
            {"user_id": "su006", "nickname": "현우", "score": 53, "rank": 6},
            {"user_id": "su007", "nickname": "유나", "score": 52, "rank": 7},
            {"user_id": "su008", "nickname": "은호", "score": 50, "rank": 8},
            {"user_id": "su009", "nickname": "다온", "score": 49, "rank": 9},
            {"user_id": "su010", "nickname": "수아", "score": 48, "rank": 10},
        ],
        "monthly": [
            {"user_id": "su011", "nickname": "민혁", "score": 70, "rank": 1},
            {"user_id": "su001", "nickname": "지훈", "score": 68, "rank": 2},
            {"user_id": "su012", "nickname": "하린", "score": 66, "rank": 3},
            {"user_id": "su013", "nickname": "산들", "score": 64, "rank": 4},
            {"user_id": "su014", "nickname": "성민", "score": 62, "rank": 5},
            {"user_id": "su015", "nickname": "소율", "score": 61, "rank": 6},
            {"user_id": "su016", "nickname": "다인", "score": 59, "rank": 7},
            {"user_id": "su017", "nickname": "로운", "score": 58, "rank": 8},
            {"user_id": "su018", "nickname": "태윤", "score": 56, "rank": 9},
            {"user_id": "su019", "nickname": "지성", "score": 54, "rank": 10},
        ],
        "season": [
            {"user_id": "su020", "nickname": "예린", "score": 82, "rank": 1},
            {"user_id": "su021", "nickname": "도윤", "score": 79, "rank": 2},
            {"user_id": "su022", "nickname": "나연", "score": 76, "rank": 3},
            {"user_id": "su023", "nickname": "준수", "score": 74, "rank": 4},
            {"user_id": "su024", "nickname": "은재", "score": 73, "rank": 5},
            {"user_id": "su025", "nickname": "도경", "score": 71, "rank": 6},
            {"user_id": "su026", "nickname": "하율", "score": 70, "rank": 7},
            {"user_id": "su027", "nickname": "산들", "score": 68, "rank": 8},
            {"user_id": "su028", "nickname": "정후", "score": 67, "rank": 9},
            {"user_id": "su029", "nickname": "정민", "score": 65, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # SQUAT
    # ---------------------------------------------------
    "squat": {
        "weekly": [
            {"user_id": "sq001", "nickname": "다은", "score": 46, "rank": 1},
            {"user_id": "sq002", "nickname": "성훈", "score": 44, "rank": 2},
            {"user_id": "sq003", "nickname": "산들", "score": 41, "rank": 3},
            {"user_id": "sq004", "nickname": "주원", "score": 40, "rank": 4},
            {"user_id": "sq005", "nickname": "정우", "score": 39, "rank": 5},
            {"user_id": "sq006", "nickname": "나린", "score": 38, "rank": 6},
            {"user_id": "sq007", "nickname": "시후", "score": 37, "rank": 7},
            {"user_id": "sq008", "nickname": "진우", "score": 36, "rank": 8},
            {"user_id": "sq009", "nickname": "예서", "score": 35, "rank": 9},
            {"user_id": "sq010", "nickname": "다흰", "score": 34, "rank": 10},
        ],
        "monthly": [
            {"user_id": "sq011", "nickname": "도하", "score": 52, "rank": 1},
            {"user_id": "sq001", "nickname": "다은", "score": 49, "rank": 2},
            {"user_id": "sq012", "nickname": "예성", "score": 47, "rank": 3},
            {"user_id": "sq013", "nickname": "승아", "score": 45, "rank": 4},
            {"user_id": "sq014", "nickname": "산들", "score": 44, "rank": 5},
            {"user_id": "sq015", "nickname": "서진", "score": 43, "rank": 6},
            {"user_id": "sq016", "nickname": "하람", "score": 42, "rank": 7},
            {"user_id": "sq017", "nickname": "다원", "score": 41, "rank": 8},
            {"user_id": "sq018", "nickname": "유림", "score": 40, "rank": 9},
            {"user_id": "sq019", "nickname": "가을", "score": 39, "rank": 10},
        ],
        "season": [
            {"user_id": "sq020", "nickname": "라희", "score": 61, "rank": 1},
            {"user_id": "sq021", "nickname": "유건", "score": 59, "rank": 2},
            {"user_id": "sq022", "nickname": "하온", "score": 58, "rank": 3},
            {"user_id": "sq023", "nickname": "하윤", "score": 56, "rank": 4},
            {"user_id": "sq024", "nickname": "산들", "score": 55, "rank": 5},
            {"user_id": "sq025", "nickname": "연우", "score": 54, "rank": 6},
            {"user_id": "sq026", "nickname": "도하", "score": 53, "rank": 7},
            {"user_id": "sq027", "nickname": "수빈", "score": 52, "rank": 8},
            {"user_id": "sq028", "nickname": "지안", "score": 51, "rank": 9},
            {"user_id": "sq029", "nickname": "서율", "score": 50, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # BALANCE
    # ---------------------------------------------------
    "balance": {
        "weekly": [
            {"user_id": "ba001", "nickname": "시윤", "score": 56, "rank": 1},
            {"user_id": "ba002", "nickname": "정우", "score": 53, "rank": 2},
            {"user_id": "ba003", "nickname": "민정", "score": 51, "rank": 3},
            {"user_id": "ba004", "nickname": "소현", "score": 50, "rank": 4},
            {"user_id": "ba005", "nickname": "주아", "score": 49, "rank": 5},
            {"user_id": "ba006", "nickname": "라온", "score": 48, "rank": 6},
            {"user_id": "ba007", "nickname": "이안", "score": 47, "rank": 7},
            {"user_id": "ba008", "nickname": "재윤", "score": 46, "rank": 8},
            {"user_id": "ba009", "nickname": "지효", "score": 45, "rank": 9},
            {"user_id": "ba010", "nickname": "서연", "score": 44, "rank": 10},
        ],
        "monthly": [
            {"user_id": "ba011", "nickname": "채린", "score": 65, "rank": 1},
            {"user_id": "ba001", "nickname": "시윤", "score": 63, "rank": 2},
            {"user_id": "ba012", "nickname": "태준", "score": 60, "rank": 3},
            {"user_id": "ba013", "nickname": "나율", "score": 58, "rank": 4},
            {"user_id": "ba014", "nickname": "다예", "score": 57, "rank": 5},
            {"user_id": "ba015", "nickname": "윤아", "score": 56, "rank": 6},
            {"user_id": "ba016", "nickname": "도하", "score": 55, "rank": 7},
            {"user_id": "ba017", "nickname": "민재", "score": 54, "rank": 8},
            {"user_id": "ba018", "nickname": "하임", "score": 53, "rank": 9},
            {"user_id": "ba019", "nickname": "연재", "score": 52, "rank": 10},
        ],
        "season": [
            {"user_id": "ba020", "nickname": "준영", "score": 72, "rank": 1},
            {"user_id": "ba021", "nickname": "나래", "score": 69, "rank": 2},
            {"user_id": "ba022", "nickname": "시아", "score": 67, "rank": 3},
            {"user_id": "ba023", "nickname": "산들", "score": 66, "rank": 4},
            {"user_id": "ba024", "nickname": "세은", "score": 64, "rank": 5},
            {"user_id": "ba025", "nickname": "지율", "score": 63, "rank": 6},
            {"user_id": "ba026", "nickname": "하원", "score": 62, "rank": 7},
            {"user_id": "ba027", "nickname": "가빈", "score": 61, "rank": 8},
            {"user_id": "ba028", "nickname": "엘라", "score": 59, "rank": 9},
            {"user_id": "ba029", "nickname": "하윤", "score": 58, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # KNEE LIFT
    # ---------------------------------------------------
    "knee_lift": {
        "weekly": [
            {"user_id": "kn001", "nickname": "도경", "score": 105, "rank": 1},
            {"user_id": "kn002", "nickname": "지아", "score": 102, "rank": 2},
            {"user_id": "kn003", "nickname": "정민", "score": 98, "rank": 3},
            {"user_id": "kn004", "nickname": "해린", "score": 96, "rank": 4},
            {"user_id": "kn005", "nickname": "승민", "score": 94, "rank": 5},
            {"user_id": "kn006", "nickname": "예나", "score": 93, "rank": 6},
            {"user_id": "kn007", "nickname": "로건", "score": 91, "rank": 7},
            {"user_id": "kn008", "nickname": "한결", "score": 89, "rank": 8},
            {"user_id": "kn009", "nickname": "윤후", "score": 88, "rank": 9},
            {"user_id": "kn010", "nickname": "태호", "score": 87, "rank": 10},
        ],
        "monthly": [
            {"user_id": "kn011", "nickname": "하람", "score": 120, "rank": 1},
            {"user_id": "kn012", "nickname": "주아", "score": 118, "rank": 2},
            {"user_id": "kn013", "nickname": "지후", "score": 114, "rank": 3},
            {"user_id": "kn014", "nickname": "아인", "score": 112, "rank": 4},
            {"user_id": "kn015", "nickname": "민서", "score": 110, "rank": 5},
            {"user_id": "kn016", "nickname": "도영", "score": 108, "rank": 6},
            {"user_id": "kn017", "nickname": "소은", "score": 106, "rank": 7},
            {"user_id": "kn018", "nickname": "정후", "score": 105, "rank": 8},
            {"user_id": "kn019", "nickname": "가빈", "score": 103, "rank": 9},
            {"user_id": "kn020", "nickname": "나희", "score": 101, "rank": 10},
        ],
        "season": [
            {"user_id": "kn021", "nickname": "하윤", "score": 135, "rank": 1},
            {"user_id": "kn022", "nickname": "가희", "score": 130, "rank": 2},
            {"user_id": "kn023", "nickname": "승준", "score": 128, "rank": 3},
            {"user_id": "kn024", "nickname": "라온", "score": 126, "rank": 4},
            {"user_id": "kn025", "nickname": "가온", "score": 124, "rank": 5},
            {"user_id": "kn026", "nickname": "보민", "score": 122, "rank": 6},
            {"user_id": "kn027", "nickname": "채우", "score": 120, "rank": 7},
            {"user_id": "kn028", "nickname": "준상", "score": 118, "rank": 8},
            {"user_id": "kn029", "nickname": "소이", "score": 116, "rank": 9},
            {"user_id": "kn030", "nickname": "유담", "score": 115, "rank": 10},
        ],
    },

    # ---------------------------------------------------
    # TRUNK FLEX
    # ---------------------------------------------------
    "trunk_flex": {
        "weekly": [
            {"user_id": "tf001", "nickname": "유진", "score": 21, "rank": 1},
            {"user_id": "tf002", "nickname": "도현", "score": 20, "rank": 2},
            {"user_id": "tf003", "nickname": "현아", "score": 18, "rank": 3},
            {"user_id": "tf004", "nickname": "하린", "score": 17, "rank": 4},
            {"user_id": "tf005", "nickname": "채아", "score": 16, "rank": 5},
            {"user_id": "tf006", "nickname": "수빈", "score": 15, "rank": 6},
            {"user_id": "tf007", "nickname": "예빈", "score": 14, "rank": 7},
            {"user_id": "tf008", "nickname": "민혁", "score": 13, "rank": 8},
            {"user_id": "tf009", "nickname": "지유", "score": 12, "rank": 9},
            {"user_id": "tf010", "nickname": "아윤", "score": 11, "rank": 10},
        ],
        "monthly": [
            {"user_id": "tf011", "nickname": "준희", "score": 25, "rank": 1},
            {"user_id": "tf001", "nickname": "유진", "score": 23, "rank": 2},
            {"user_id": "tf012", "nickname": "해린", "score": 22, "rank": 3},
            {"user_id": "tf013", "nickname": "재이", "score": 21, "rank": 4},
            {"user_id": "tf014", "nickname": "도하", "score": 20, "rank": 5},
            {"user_id": "tf015", "nickname": "유리", "score": 19, "rank": 6},
            {"user_id": "tf016", "nickname": "나율", "score": 18, "rank": 7},
            {"user_id": "tf017", "nickname": "연우", "score": 17, "rank": 8},
            {"user_id": "tf018", "nickname": "성하", "score": 15, "rank": 9},
            {"user_id": "tf019", "nickname": "정후", "score": 14, "rank": 10},
        ],
        "season": [
            {"user_id": "tf020", "nickname": "소민", "score": 28, "rank": 1},
            {"user_id": "tf021", "nickname": "예준", "score": 26, "rank": 2},
            {"user_id": "tf022", "nickname": "지유", "score": 25, "rank": 3},
            {"user_id": "tf023", "nickname": "지안", "score": 24, "rank": 4},
            {"user_id": "tf024", "nickname": "규민", "score": 23, "rank": 5},
            {"user_id": "tf025", "nickname": "하율", "score": 22, "rank": 6},
            {"user_id": "tf026", "nickname": "소이", "score": 21, "rank": 7},
            {"user_id": "tf027", "nickname": "리안", "score": 20, "rank": 8},
            {"user_id": "tf028", "nickname": "하람", "score": 19, "rank": 9},
            {"user_id": "tf029", "nickname": "로아", "score": 18, "rank": 10},
        ],
    },
}




# ======================================================================
# 6. 등급/측정/결과 관련 상수
# ======================================================================

GRADE_INFO = {
    "1등급": {"min": 90, "color": COLORS["DARK_BLUE"], "desc": "최고 등급"},
    "2등급": {"min": 80, "color": COLORS["MAIN_BLUE"], "desc": "우수 등급"},
    "3등급": {"min": 70, "color": COLORS["ACCENT_BLUE"], "desc": "양호 등급"},
    "4등급": {"min": 60, "color": COLORS["MEDIUM_BLUE"], "desc": "보통 등급"},
    "5등급": {"min": 0,  "color": COLORS["LIGHT_BLUE"], "desc": "기본 등급"},
}

EVENT_DISPLAY_NAME = {
    "pushup": "팔굽혀펴기",
    "situp": "윗몸일으키기",
    "squat": "스쿼트",
    "balance": "외발서기",
    "knee_lift": "제자리 무릎들기",
    "trunk_flex": "상체 기울기"
}


# ======================================================================
# 7. 운동 종목 상세 정보 (튜토리얼/설명/아이콘 포함)
# ======================================================================

EXERCISES = {
    "pushup": {
        "name": "팔굽혀펴기",
        "description": "상체 근지구력을 측정합니다",
        "tutorial_description": "상체 근력을 측정합니다",
        "duration_label": "약 1분",
        "difficulty_label": "2/3",
        "icon": "💪",
        "instructions": [
            "양손을 어깨너비로 벌리고 바닥에 댑니다",
            "몸을 일직선으로 유지합니다",
            "팔꿈치를 90도까지 구부렸다 펴세요",
            "가슴이 바닥에 거의 닿을 때까지 내려갑니다"
        ]
    },

    "situp": {
        "name": "윗몸일으키기",
        "description": "복근 근력을 측정합니다",
        "tutorial_description": "복근 근력을 측정합니다",
        "duration_label": "약 1분 30초",
        "difficulty_label": "2/3",
        "icon": "🔥",
        "instructions": [
            "바닥에 누워 무릎을 구부립니다",
            "양손을 귀 뒤에 댑니다",
            "상체를 일으켜 무릎에 닿을 때까지 올립니다",
            "천천히 원래 자세로 돌아갑니다"
        ]
    },

    "squat": {
        "name": "스쿼트",
        "description": "하체 근력과 리듬감을 측정합니다",
        "tutorial_description": "하체 근력과 리듬감을 측정합니다",
        "duration_label": "약 1분",
        "difficulty_label": "1/3",
        "icon": "🦵",
        "instructions": [
            "발을 어깨너비로 벌립니다",
            "무릎을 구부려 엉덩이를 내립니다",
            "무릎이 발가락을 넘지 않도록 주의합니다",
            "일어서서 원래 자세로 돌아갑니다"
        ]
    },

    "balance": {
        "name": "외발서기",
        "description": "균형감각과 근지구력을 측정합니다",
        "tutorial_description": "균형감각과 근지구력을 측정합니다",
        "duration_label": "약 1분",
        "difficulty_label": "3/3",
        "icon": "⚖️",
        "instructions": [
            "한 발로 서서 균형을 잡습니다",
            "다른 발은 바닥에서 들어올립니다",
            "몸을 일직선으로 유지합니다",
            "가능한 오래 균형을 유지합니다"
        ]
    },

    "knee_lift": {
        "name": "제자리 무릎들기",
        "description": "하체 근력과 유연성을 측정합니다",
        "tutorial_description": "하체 근력과 유연성을 측정합니다",
        "duration_label": "약 1분",
        "difficulty_label": "1/3",
        "icon": "🏃",
        "instructions": [
            "똑바로 서서 시작합니다",
            "한쪽 무릎을 가슴 쪽으로 들어올립니다",
            "반대편 팔을 앞으로 뻗습니다",
            "원래 자세로 돌아가 반대편도 반복합니다"
        ]
    },

    "trunk_flex": {
        "name": "상체 기울기",
        "description": "유연성과 근력을 측정합니다",
        "tutorial_description": "유연성과 근력을 측정합니다",
        "duration_label": "약 30초",
        "difficulty_label": "2/3",
        "icon": "🧘",
        "instructions": [
            "똑바로 서서 시작합니다",
            "상체를 앞으로 천천히 기울입니다",
            "무릎을 구부리지 않고 유지합니다",
            "가능한 한 아래로 내려간 후 원래 자세로 돌아갑니다"
        ]
    }
}
