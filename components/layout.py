"""
레이아웃 컴포넌트 모듈 (하위 호환성 유지)

⚠️ 이 파일은 하위 호환성을 위해 유지됩니다.
새로운 코드에서는 각 컴포넌트를 해당 모듈에서 직접 import하세요:

- 공통 컴포넌트: from components.common import ProfileAvatar
- 홈 페이지: from components.cards.home_card import GreetingCard, ActionButtonGrid, ResultSummaryCard, FeedItem
- 랭킹 페이지: from components.cards.rank_card import MyRankCard, RankCard
- 프로필 페이지: from components.cards.profile_card import StatCard, BadgeCard, GradeProgressBar, GradeCard, PointsCard, ActionButtonsRow
- app.py 전용: from components.common.cards import FeatureCard, ExerciseCarouselCard, ExerciseCarousel
"""

# 공통 컴포넌트
from components.common import ProfileAvatar

# SectionCard와 CloseSectionCard는 section_card.py에 있음
from components.common.section_card import SectionCard, CloseSectionCard

# 홈 페이지 컴포넌트
from components.cards.home_card import (
    GreetingCard,
    ActionButtonGrid,
    ResultSummaryCard,
    FeedItem
)

# 랭킹 페이지 컴포넌트
from components.cards.rank_card import MyRankCard, RankCard

# 프로필 페이지 컴포넌트
from components.cards.profile_card import (
    StatCard,
    BadgeCard,
    GradeProgressBar,
    GradeCard,
    PointsCard,
    ActionButtonsRow
)

# app.py 전용 컴포넌트
from components.common.cards import FeatureCard, ExerciseCarouselCard, ExerciseCarousel

# 하위 호환성을 위해 모든 컴포넌트를 export
__all__ = [
    # 공통
    "ProfileAvatar",
    "SectionCard",
    "CloseSectionCard",
    # 홈 페이지
    "GreetingCard",
    "ActionButtonGrid",
    "ResultSummaryCard",
    "FeedItem",
    # 랭킹 페이지
    "MyRankCard",
    "RankCard",
    # 프로필 페이지
    "StatCard",
    "BadgeCard",
    "GradeProgressBar",
    "GradeCard",
    "PointsCard",
    "ActionButtonsRow",
    # app.py 전용
    "FeatureCard",
    "ExerciseCarouselCard",
    "ExerciseCarousel",
]
