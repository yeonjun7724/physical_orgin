"""서비스 인스턴스 캐싱 유틸리티"""
import streamlit as st
from service import (
    ProfileService, ResultService, BadgeService, UserBadgeService,
    PointsService, LeaderboardService, StreakService, NotificationService,
    InventoryService
)


def get_service(service_class):
    """서비스 인스턴스를 캐싱하여 반환
    
    사용 예시:
        profile_service = get_service(ProfileService)
    """
    service_name = service_class.__name__
    cache_key = f"_service_{service_name}"
    
    if cache_key not in st.session_state:
        st.session_state[cache_key] = service_class()
    
    return st.session_state[cache_key]


# 편의 함수들
def get_profile_service():
    return get_service(ProfileService)


def get_result_service():
    return get_service(ResultService)


def get_badge_service():
    return get_service(BadgeService)


def get_user_badge_service():
    return get_service(UserBadgeService)


def get_points_service():
    return get_service(PointsService)


def get_leaderboard_service():
    return get_service(LeaderboardService)


def get_streak_service():
    return get_service(StreakService)


def get_notification_service():
    return get_service(NotificationService)


def get_inventory_service():
    return get_service(InventoryService)

