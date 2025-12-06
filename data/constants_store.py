STORE_BADGES = [
  {
    "badge_id": "badge_001",
    "name": "연속 3일 측정",
    "description": "3일 연속으로 운동을 측정하세요",
    "icon": "🔥",
    "condition": {
      "type": "streak",
      "value": 3
    },
    "reward": 50,
    "category": "streak"
  },
  {
    "badge_id": "badge_002",
    "name": "연속 7일 측정",
    "description": "7일 연속으로 운동을 측정하세요",
    "icon": "💪",
    "condition": {
      "type": "streak",
      "value": 7
    },
    "reward": 150,
    "category": "streak"
  },
  {
    "badge_id": "badge_003",
    "name": "연속 30일 측정",
    "description": "30일 연속으로 운동을 측정하세요",
    "icon": "👑",
    "condition": {
      "type": "streak",
      "value": 30
    },
    "reward": 500,
    "category": "streak"
  },
  {
    "badge_id": "badge_004",
    "name": "1등급 달성",
    "description": "어떤 운동에서든 1등급을 달성하세요",
    "icon": "⭐",
    "condition": {
      "type": "grade",
      "value": "1등급"
    },
    "reward": 100,
    "category": "achievement"
  },
  {
    "badge_id": "badge_005",
    "name": "올라운더",
    "description": "모든 운동 종목을 한 번씩 측정하세요",
    "icon": "🏆",
    "condition": {
      "type": "all_exercises",
      "exercises": [
        "pushup",
        "situp",
        "squat",
        "balance",
        "knee_lift",
        "trunkFlex"
      ]
    },
    "reward": 200,
    "category": "achievement"
  },
  {
    "badge_id": "badge_006",
    "name": "팔굽혀펴기 마스터",
    "description": "팔굽혀펴기에서 10회 이상 측정하세요",
    "icon": "💪",
    "condition": {
      "type": "exercise_count",
      "exercise": "pushup",
      "value": 10
    },
    "reward": 80,
    "category": "exercise"
  },
  {
    "badge_id": "badge_007",
    "name": "랭킹 10위 안",
    "description": "주간 랭킹에서 10위 안에 들어가세요",
    "icon": "🎯",
    "condition": {
      "type": "ranking",
      "period": "weekly",
      "max_rank": 10
    },
    "reward": 300,
    "category": "ranking"
  },
  {
    "badge_id": "badge_008",
    "name": "첫 측정",
    "description": "첫 번째 운동 측정을 완료하세요",
    "icon": "🎉",
    "condition": {
      "type": "first_measurement"
    },
    "reward": 20,
    "category": "milestone"
  },
  {
    "badge_id": "badge_009",
    "name": "100회 측정",
    "description": "총 100회의 운동 측정을 완료하세요",
    "icon": "💯",
    "condition": {
      "type": "total_measurements",
      "value": 100
    },
    "reward": 400,
    "category": "milestone"
  },
  {
    "badge_id": "badge_010",
    "name": "완벽한 정확도",
    "description": "측정 정확도 95% 이상을 달성하세요",
    "icon": "🎯",
    "condition": {
      "type": "accuracy",
      "value": 0.95
    },
    "reward": 150,
    "category": "achievement"
  }
]


STORE_AVATARS = [
  {
    "avatar_id": "avatar_001",
    "name": "기본 아바타",
    "description": "기본 제공 아바타",
    "icon": "👤",
    "price": 0,
    "owned": True
  },{
    "avatar_id": "avatar_002",
    "name": "운동맨",
    "description": "근육질 아바타",
    "icon": "💪",
    "price": 500,
    "owned": False
  },
  {
    "avatar_id": "avatar_003",
    "name": "요가마스터",
    "description": "요가 전문가 아바타",
    "price": 600,
    "icon": "🧘",
    "owned": False
  },
  {
    "avatar_id": "avatar_005",
    "name": "달리기왕",
    "description": "러닝 전문가 아바타",
    "price": 550,
    "icon": "🏃",
    "desc": "러닝 전문가 아바타",
    "owned": false
  },
  {
    "avatar_id": "avatar_004",
    "name": "수영선수",
    "description": "수영 전문가 아바타",
    "price": 700,
    "icon": "🏊",
    "desc": "수영 전문가 아바타",
    "owned": false
  },
  {
    "avatar_id": "avatar_006",
    "name": "복싱챔피언",
    "description": "복싱 전문가 아바타",
    "price": 800,
    "icon": "🥊",
    "desc": "복싱 전문가 아바타",
    "owned": false
  },
  {
    "avatar_id": "avatar_007",
    "name": "골든아바타",
    "description": "프리미엄 골든 아바타",
    "price": 1000,
    "icon": "⭐",
    "desc": "프리미엄 골든 아바타",
    "owned": false
  },
  {
    "avatar_id": "avatar_008",
    "name": "레전드",
    "price": 1500,
    "icon": "👑",
    "desc": "최고급 레전드 아바타",
    "owned": false
  },
  {
    "avatar_id": "avatar_009",
    "name": "미래전사",
    "price": 1200,
    "icon": "🤖",
    "desc": "미래형 아바타",
    "owned": false
  }
]
STORE_FRAMES = [
  {
    "name": "기본 프레임",
    "price": 0,
    "icon": "📄",
    "desc": "기본 제공 프레임",
    "owned": true
  },
  {
    "name": "골든 프레임",
    "price": 300,
    "icon": "✨",
    "desc": "황금색 테두리 프레임",
    "owned": false
  },
  {
    "name": "레인보우 프레임",
    "price": 400,
    "icon": "🌈",
    "desc": "무지개색 프레임",
    "owned": false
  },
  {
    "name": "네온 프레임",
    "price": 500,
    "icon": "💡",
    "desc": "네온 효과 프레임",
    "owned": false
  },
  {
    "name": "크리스탈 프레임",
    "price": 600,
    "icon": "💎",
    "desc": "수정 같은 프레임",
    "owned": false
  },
  {
    "name": "플레임 프레임",
    "price": 700,
    "icon": "🔥",
    "desc": "불꽃 효과 프레임",
    "owned": false
  },
  {
    "name": "스타 프레임",
    "price": 800,
    "icon": "⭐",
    "desc": "별빛 효과 프레임",
    "owned": false
  },
  {
    "name": "로열 프레임",
    "price": 1000,
    "icon": "👑",
    "desc": "왕관 프레임",
    "owned": false
  },
  {
    "name": "레전드 프레임",
    "price": 1500,
    "icon": "🏆",
    "desc": "최고급 레전드 프레임",
    "owned": false
  }
]
