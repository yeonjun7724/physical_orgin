"""프로필 페이지"""
import streamlit as st
import pandas as pd
from utils.app_common import setup_common
from components.common import PageHeader, ProfileAvatar
from components.common.section_card import SectionCard, CloseSectionCard
from components.profile import (
   StatCard, BadgeCard, GradeProgressBar, GradeCard, PointsCard, ActionButtonsRow
)
from service import (
   ProfileService, ResultService, BadgeService, UserBadgeService,
   PointsService, LeaderboardService, StreakService
)
from utils.constants import COLORS, GRADE_INFO

# 공통 설정 적용
setup_common()


def render(go_to):
   """프로필 페이지 렌더링"""
   from utils.page_utils import get_user_id
   user_id = get_user_id()
   if not user_id:
      st.warning("로그인이 필요합니다.")
      return
   
   from utils.service_cache import (
      get_profile_service, get_result_service, get_badge_service,
      get_user_badge_service, get_points_service, get_leaderboard_service
   )
   profile_service = get_profile_service()
   result_service = get_result_service()
   badge_service = get_badge_service()
   user_badge_service = get_user_badge_service()
   points_service = get_points_service()
   leaderboard_service = get_leaderboard_service()
   
   # 프로필 정보 가져오기
   profile = profile_service.get_profile_by_user_id(user_id)
   if not profile:
      st.warning("프로필 정보가 없습니다.")
      return
   
   # 통계 계산
   results = result_service.get_results_by_user(user_id)
   avg_score = int(sum(r.get("raw_score", 0) for r in results) / len(results)) if results else 0
   
   # 랭킹 가져오기 (주간 pushup 기준)
   my_rank_entry = leaderboard_service.get_user_rank(user_id, "pushup", "weekly")
   rank = my_rank_entry.get("rank", 0) if my_rank_entry else 0
   
   # 포인트 가져오기
   user_points = points_service.get_user_points(user_id)
   total_points = user_points.get("total_points", 0) if user_points else 0
   
   
   # 첫 번째 행: 프로필 사진 / 키몸무게 / FIT포인트
   col1, col2, col3 = st.columns(3)
   
   with col1:
      # 프로필 사진 영역
      ProfileAvatar(
         profile.get("nickname", "사용자"),
         profile.get("age_group", "20대"),
         "남성" if profile.get("gender") == "M" else "여성",
         level=100,
         show_info=False
      )
   
   with col2:
      # 키, 몸무게, 나이, 성별, 레벨 정보
      user_age = profile.get("age_group", "20대")
      user_gender = "남성" if profile.get("gender") == "M" else "여성"
      user_height = st.session_state.get("user_height", 175)
      user_weight = st.session_state.get("user_weight", 70)
      user_level = 100
      
      st.info(
         f"**키:** {user_height} cm  \n"
         f"**몸무게:** {user_weight} kg  \n"
         f"**나이:** {user_age}  \n"
         f"**성별:** {user_gender}  \n"
         f"**레벨:** Lv. {user_level}"
      )
   
   with col3:
      # FIT 포인트
      PointsCard(total_points, "FIT 포인트")
   
   # 두 번째 행: 프로필사진변경 / 내정보수정 버튼
   btn_col1, btn_col2 = st.columns(2)
   
   with btn_col1:
      if st.button("프로필 사진 변경", use_container_width=True):
         st.info("프로필 사진 변경 기능은 준비 중입니다.")
   
   with btn_col2:
      if st.button("내정보 수정", use_container_width=True, type="primary"):
         st.switch_page("other_pages/confirm_to_info_update.py")
   
   # 세 번째 행: 종합점수 / 현재등급 / 전체순위
   stat_col1, stat_col2, stat_col3 = st.columns(3)
   
   with stat_col1:
      StatCard(f"{avg_score}점", "종합 점수", COLORS["MAIN_BLUE"])
   
   with stat_col2:
      StatCard("2등급", "현재 등급", COLORS["MAIN_BLUE"])
   
   with stat_col3:
      StatCard(f"{rank}위", "전체 순위", COLORS["ACCENT_BLUE"])
   
   
   # 등급 정보
   SectionCard("⭐ 등급 정보")
   
   # 등급 진행도
   current_grade = "2등급"
   next_grade = "1등급"
   progress = 75  # 다음 등급까지 75%
   GradeProgressBar(current_grade, next_grade, progress)
   
   # 등급 설명
   cols = st.columns(5)
   for idx, (grade, info) in enumerate(GRADE_INFO.items()):
      with cols[idx]:
         GradeCard(
            grade=grade,
            min_score=info['min'],
            desc=info['desc'],
            color=info['color'],
            is_current=(grade == current_grade)
         )
   
   CloseSectionCard()
   
   # 뱃지 섹션
   SectionCard("🏅 뱃지 & 칭호")
   
   # 사용자가 획득한 배지
   user_badges = user_badge_service.get_user_badges(user_id)
   earned_badge_ids = {ub.get("badge_id") for ub in user_badges}
   
   # 모든 배지 가져오기
   all_badges = badge_service.get_all_badges()
   
   badge_cols = st.columns(3)
   for idx, badge in enumerate(all_badges[:6]):  # 최대 6개만 표시
      with badge_cols[idx % 3]:
         badge_id = badge.get("badge_id")
         earned = badge_id in earned_badge_ids
         BadgeCard(
            name=badge.get("name", ""),
            icon=badge.get("icon", "🏅"),
            desc=badge.get("description", ""),
            earned=earned
         )
   
   CloseSectionCard()
   
   # 측정 히스토리
   SectionCard("📈 측정 히스토리")
   
   # 히스토리 데이터 가져오기
   if results:
      history_data = {
         "날짜": [],
         "종목": [],
         "점수": [],
         "등급": [],
         "정확도": [],
      }
      
      # 최신순으로 정렬
      sorted_results = sorted(results, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
      
      for result in sorted_results:
         created_at = result.get("created_at", "")
         date_str = created_at.split("T")[0] if "T" in created_at else created_at
         history_data["날짜"].append(date_str)
         history_data["종목"].append(result.get("event", ""))
         history_data["점수"].append(result.get("raw_score", 0))
         history_data["등급"].append(result.get("official_grade", "5등급"))
         accuracy = result.get("accuracy", 0)
         history_data["정확도"].append(f"{int(accuracy * 100)}%")
      
      df_history = pd.DataFrame(history_data)
      
      st.dataframe(
         df_history,
         use_container_width=True,
         hide_index=True,
         column_config={
            "날짜": st.column_config.TextColumn("날짜", width="medium"),
            "종목": st.column_config.TextColumn("종목", width="medium"),
            "점수": st.column_config.NumberColumn("점수", width="small", format="%d점"),
            "등급": st.column_config.TextColumn("등급", width="small"),
            "정확도": st.column_config.TextColumn("정확도", width="small"),
         }
      )
   else:
      st.info("측정 히스토리가 없습니다.")
   
   if st.button("더 보기", key="view_more_history", use_container_width=True):
      st.info("더 많은 히스토리를 보려면 스크롤하세요.")
   
   CloseSectionCard()
   
   # 설정 버튼
   ActionButtonsRow([
      {
         "label": "⚙️ 설정",
         "key": "settings",
         "on_click": lambda: st.info("설정 페이지로 이동합니다. (권한/프라이버시/데이터 내보내기)")
      },
      {
         "label": "📤 결과 공유",
         "key": "share_result",
         "on_click": lambda: st.success("스크린샷이 생성되었습니다! 결과를 공유하세요.")
      }
   ])


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
