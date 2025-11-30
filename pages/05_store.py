"""상점 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common.section_card import SectionCard, CloseSectionCard
from components.cards.store_card import StoreItemGrid
from service import PointsService

# 공통 설정 적용
setup_common()


def render(go_to):
   """상점 페이지 렌더링"""
   from utils.page_utils import get_user_id
   user_id = get_user_id()
   if not user_id:
      st.warning("로그인이 필요합니다.")
      return
   
   from utils.service_cache import get_points_service
   points_service = get_points_service()
   
   # 현재 포인트 표시
   current_points = points_service.get_total_points(user_id)
   
   # 보유 포인트 표시 (큰 폰트)
   st.markdown(
      f"""
      <div style="background-color: #E3F2FD; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #4c84af;">
         <div style="font-size: 1.5rem; font-weight: 700; color: #4c84af; margin-bottom: 0.5rem;">
            💰 보유 포인트: {current_points:,} FIT
         </div>
         <div style="font-size: 0.9rem; color: #666;">
            포인트는 측정과 챌린지 완료로 획득할 수 있습니다
         </div>
      </div>
      """,
      unsafe_allow_html=True
   )
   
   # 탭 폰트 크기 스타일
   st.markdown(
      """
      <style>
      button[data-baseweb="tab"] {
         font-size: 1.1rem !important;
         font-weight: 600 !important;
         padding: 0.75rem 1.5rem !important;
      }
      </style>
      """,
      unsafe_allow_html=True
   )
   
   # 탭으로 아바타/프레임 전환
   tab1, tab2 = st.tabs(["👤 아바타", "🖼️ 프레임"])
   
   with tab1:
      st.caption("프로필에 표시되는 아바타를 선택하세요.")
      
      avatars = [
         {"name": "기본 아바타", "price": 0, "icon": "👤", "desc": "기본 제공 아바타", "owned": True},
         {"name": "운동맨", "price": 500, "icon": "💪", "desc": "근육질 아바타", "owned": False},
         {"name": "요가마스터", "price": 600, "icon": "🧘", "desc": "요가 전문가 아바타", "owned": False},
         {"name": "달리기왕", "price": 550, "icon": "🏃", "desc": "러닝 전문가 아바타", "owned": False},
         {"name": "수영선수", "price": 700, "icon": "🏊", "desc": "수영 전문가 아바타", "owned": False},
         {"name": "복싱챔피언", "price": 800, "icon": "🥊", "desc": "복싱 전문가 아바타", "owned": False},
         {"name": "골든아바타", "price": 1000, "icon": "⭐", "desc": "프리미엄 골든 아바타", "owned": False},
         {"name": "레전드", "price": 1500, "icon": "👑", "desc": "최고급 레전드 아바타", "owned": False},
         {"name": "미래전사", "price": 1200, "icon": "🤖", "desc": "미래형 아바타", "owned": False},
      ]
      
      StoreItemGrid(avatars, category="아바타")
   
   with tab2:
      st.caption("결과 공유 시 사용할 프레임을 선택하세요.")
      
      frames = [
         {"name": "기본 프레임", "price": 0, "icon": "📄", "desc": "기본 제공 프레임", "owned": True},
         {"name": "골든 프레임", "price": 300, "icon": "✨", "desc": "황금색 테두리 프레임", "owned": False},
         {"name": "레인보우 프레임", "price": 400, "icon": "🌈", "desc": "무지개색 프레임", "owned": False},
         {"name": "네온 프레임", "price": 500, "icon": "💡", "desc": "네온 효과 프레임", "owned": False},
         {"name": "크리스탈 프레임", "price": 600, "icon": "💎", "desc": "수정 같은 프레임", "owned": False},
         {"name": "플레임 프레임", "price": 700, "icon": "🔥", "desc": "불꽃 효과 프레임", "owned": False},
         {"name": "스타 프레임", "price": 800, "icon": "⭐", "desc": "별빛 효과 프레임", "owned": False},
         {"name": "로열 프레임", "price": 1000, "icon": "👑", "desc": "왕관 프레임", "owned": False},
         {"name": "레전드 프레임", "price": 1500, "icon": "🏆", "desc": "최고급 레전드 프레임", "owned": False},
      ]
      
      StoreItemGrid(frames, category="프레임")
   
   # 구매 안내
   st.info("💡 **팁**: FIT 포인트는 측정 완료, 챌린지 달성, 랭킹 보상으로 획득할 수 있습니다!")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
