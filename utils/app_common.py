"""공통 설정 및 유틸리티"""
import streamlit as st
from service import (
   InventoryService, PointsService, ProfileService, 
   StreakService, NotificationService
)
import utils.style as style


def setup_common():
   """공통 설정 적용 (모든 페이지에서 사용)"""
   st.markdown("""
   <style>

   /* 스트림릿이 자동으로 삽입하는 페이지 최상단 공백 제거 */
   section.main > div:nth-child(1) {
      padding-top: 0 !important;
      margin-top: 0 !important;
   }

   /* stVerticalBlock 자체를 숨김 */
   div[data-testid="stVerticalBlock"] {
      margin-top: 0 !important;
      padding-top: 0 !important;
   }

   </style>
   """, unsafe_allow_html=True)


   # 헤더 렌더링 플래그 리셋 (매 실행마다)
   st.session_state._header_rendered_this_run = False
   
   # user_id 확인
   user_id = st.session_state.get("user_id")
   if not user_id:
      return
   
   # 서비스 인스턴스 생성
   inventory_service = InventoryService()
   points_service = PointsService()
   profile_service = ProfileService()
   streak_service = StreakService()
   notification_service = NotificationService()
   
   # 포인트 초기화 (없으면 생성)
   if not points_service.get_user_points(user_id):
      points_service.initialize_user_points(user_id)
   
   # 포인트를 session_state에 로드
   user_points = points_service.get_user_points(user_id)
   st.session_state.user_points = user_points.get("total_points", 0) if user_points else 0
   
   # 인벤토리 초기화 (없으면 기본 아이템 추가)
   inventory = inventory_service.get_user_inventory(user_id)
   if not inventory:
      # 기본 아이템 추가
      inventory_service.add_item(user_id, "기본 아바타", "아바타", "👤", "기본 제공 아바타", 0, "default")
      inventory_service.add_item(user_id, "기본 프레임", "프레임", "📄", "기본 제공 프레임", 0, "default")
      inventory_service.equip_item(user_id, "기본 아바타")
      inventory_service.equip_item(user_id, "기본 프레임")
      inventory = inventory_service.get_user_inventory(user_id)
   
   # 보관함을 session_state에 로드 (기존 형식 유지)
   st.session_state.my_storage = [
      {
         "name": item.get("item_name"),
         "category": item.get("item_category"),
         "icon": item.get("item_icon"),
         "desc": item.get("item_description"),
         "price": item.get("price"),
         "equipped": item.get("equipped", False)
      }
      for item in inventory
   ]
   
   # 착용 상태 초기화
   equipped_avatar = inventory_service.get_equipped_item(user_id, "아바타")
   st.session_state.equipped_avatar = equipped_avatar.get("item_name") if equipped_avatar else "기본 아바타"
   
   equipped_frame = inventory_service.get_equipped_item(user_id, "프레임")
   st.session_state.equipped_frame = equipped_frame.get("item_name") if equipped_frame else "기본 프레임"
   
   # 프로필 정보 로드
   profile = profile_service.get_profile_by_user_id(user_id)
   if profile:
      st.session_state.user_age = profile.get("age_group", "20대")
      st.session_state.user_gender = "남성" if profile.get("gender") == "M" else "여성"
   
   # 연속 측정 초기화
   if not streak_service.get_user_streak(user_id):
      streak_service.initialize_streak(user_id)
   
   # 알림 설정 초기화
   if not notification_service.get_user_settings(user_id):
      notification_service.initialize_settings(user_id)
   
   # 페이지 설정 - 사이드바 활성화
   # 전역 스타일 적용
   style.apply_global_css()
   

