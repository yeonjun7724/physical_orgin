"""랭킹 페이지"""
import streamlit as st
import pandas as pd
from utils.app_common import setup_common
from components.common import PageHeader
from components.common.section_card import SectionCard, CloseSectionCard
from components.ranking import MyRankCard, RankCard
# 서비스는 필요할 때 service_cache에서 가져옴
from utils.constants import COLORS, EXERCISES

# 공통 설정 적용
setup_common()


def _generate_mock_leaderboard(event: str, period: str, limit: int) -> list:
   """임시 랭킹 데이터 생성"""
   import random
   
   mock_names = [
      "체력왕김철수", "운동마스터", "피트니스킹", "헬스장주인", "근육맨",
      "스포츠스타", "운동러버", "피트니스퀸", "헬스여왕", "체력부자",
      "운동고수", "피트니스프로", "헬스마니아", "체력천재", "운동신",
      "피트니스신", "헬스고수", "체력달인", "운동왕", "피트니스킹"
   ]
   
   age_groups = ["20-24", "25-29", "30-34", "35-39", "40-44"]
   genders = ["M", "F"]
   
   # 운동 종목별 기본 점수 범위
   score_ranges = {
      "pushup": (30, 80),
      "situp": (25, 70),
      "squat": (35, 85),
      "balance": (20, 60),
      "kneelift": (40, 90),
      "trunkFlex": (15, 50)
   }
   
   min_score, max_score = score_ranges.get(event, (30, 70))
   
   mock_data = []
   for i in range(limit):
      rank = i + 1
      score = max_score - (i * 2) + random.randint(-3, 3)
      score = max(min_score, min(max_score, score))  # 범위 내로 제한
      
      mock_data.append({
         "event": event,
         "period": period,
         "user_id": f"mock_user_{i+1}",
         "score": score,
         "rank": rank,
         "age_group": random.choice(age_groups),
         "gender": random.choice(genders),
         "nickname": mock_names[i % len(mock_names)] if i < len(mock_names) else f"사용자{i+1}"
      })
   
   return mock_data


def render(go_to):
   """랭킹 페이지 렌더링"""
   from utils.page_utils import get_user_id
   user_id = get_user_id()
   if not user_id:
      st.warning("로그인이 필요합니다.")
      return
   
   from utils.service_cache import get_leaderboard_service, get_profile_service, get_result_service
   leaderboard_service = get_leaderboard_service()
   profile_service = get_profile_service()
   result_service = get_result_service()
   
   # 필터 섹션
   SectionCard("🔍 필터")
   
   # 운동 종목 버튼 선택
   st.markdown("**운동 종목**")
   
   # 운동 종목 매핑 (key -> 한국어 이름)
   event_mapping = {
      "전체": "전체",
      "pushup": "팔굽혀펴기",
      "situp": "윗몸일으키기",
      "squat": "스쿼트 리듬",
      "balance": "외발서기",
      "kneelift": "제자리 무릎들기",
      "trunkFlex": "상체 기울기"
   }
   
   # 현재 선택된 운동 종목 (기본값: "전체")
   if "ranking_event" not in st.session_state:
      st.session_state.ranking_event = "전체"
   
   # 버튼 크기 통일을 위한 CSS
   st.markdown(
      """
      <style>
      button[data-testid*="event_btn_"] {
         min-width: 130px !important;
         width: 100% !important;
      }
      </style>
      """,
      unsafe_allow_html=True
   )
   
   # 버튼들을 가로로 배치
   event_keys = list(event_mapping.keys())
   event_cols = st.columns(len(event_keys))
   
   for idx, event_key in enumerate(event_keys):
      with event_cols[idx]:
         # 선택된 버튼은 primary 타입으로 표시
         button_type = "primary" if st.session_state.ranking_event == event_key else "secondary"
         if st.button(
            event_mapping[event_key],
            key=f"event_btn_{event_key}",
            use_container_width=True,
            type=button_type
         ):
            st.session_state.ranking_event = event_key
            st.rerun()
   
   event = st.session_state.ranking_event
   
   col1, col2 = st.columns(2)
   
   with col1:
      # 기간 선택
      period = st.selectbox(
         "기간",
         ["weekly", "monthly", "all_time"],
         key="ranking_period",
         help="기간별 랭킹을 확인할 수 있습니다"
      )
   
   with col2:
      # 표시할 개수
      limit = st.selectbox(
         "표시 개수",
         [10, 20, 50, 100],
         key="ranking_limit",
         help="표시할 랭킹 개수를 선택하세요"
      )
   
   CloseSectionCard()
   
   # 내 순위 카드
   my_rank = None
   my_score = 0
   if event != "전체":
      my_rank = leaderboard_service.get_user_rank(user_id, event, period)
      if my_rank:
         my_score = my_rank.get("score", 0)
         rank = my_rank.get("rank", 0)
      else:
         rank = 0
   else:
      # 전체 종목 평균 점수 계산
      all_results = result_service.get_results_by_user(user_id)
      if all_results:
         my_score = int(sum(r.get("raw_score", 0) for r in all_results) / len(all_results))
      rank = 0
   
   MyRankCard(
      rank=rank,
      percentile=str(my_rank.get("percentile", 0)) if my_rank else "0",
      total_score=my_score,
      grade="2등급",  # TODO: 등급 계산
      reward="주간 보상: +200 FIT"
   )
   
   # 랭킹 테이블
   SectionCard("📊 랭킹 목록")
   
   if event == "전체":
      st.info("운동 종목을 선택해주세요.")
   else:
      # 랭킹 데이터 가져오기
      leaderboard = leaderboard_service.get_top_rankings(event, period, limit)
      
      if leaderboard:
         # 프로필 정보 가져오기
         ranking_data = []
         for entry in leaderboard:
            # 임시 데이터인 경우 nickname이 이미 있음
            if "nickname" in entry:
               nickname = entry["nickname"]
            else:
               profile = profile_service.get_profile_by_user_id(entry.get("user_id"))
               nickname = profile.get("nickname", "알 수 없음") if profile else "알 수 없음"
            
            ranking_data.append({
               "순위": entry.get("rank", 0),
               "닉네임": nickname,
               "총점": entry.get("score", 0),
               "등급": "1등급",  # TODO: 등급 계산
               "연령대": entry.get("age_group", ""),
               "성별": "남성" if entry.get("gender") == "M" else "여성",
            })
         
         df = pd.DataFrame(ranking_data)
         
         # 상위 3명 특별 표시
         top3 = leaderboard[:3]
         top3_cols = st.columns(3)
         for idx, entry in enumerate(top3):
            with top3_cols[idx]:
               # 임시 데이터인 경우 nickname이 이미 있음
               if "nickname" in entry:
                  name = entry["nickname"]
               else:
                  profile = profile_service.get_profile_by_user_id(entry.get("user_id"))
                  name = profile.get("nickname", "알 수 없음") if profile else "알 수 없음"
               
               RankCard(
                  rank=entry.get("rank", 0),
                  name=name,
                  score=f"{entry.get('score', 0)}점"
               )
         
         # 랭킹 테이블
         st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
               "순위": st.column_config.NumberColumn("순위", width="small"),
               "닉네임": st.column_config.TextColumn("닉네임", width="medium"),
               "총점": st.column_config.NumberColumn("총점", width="small", format="%d점"),
               "등급": st.column_config.TextColumn("등급", width="small"),
               "연령대": st.column_config.TextColumn("연령대", width="small"),
               "성별": st.column_config.TextColumn("성별", width="small"),
            }
         )
      else:
         st.info("랭킹 데이터가 없습니다.")
   
   CloseSectionCard()
   
   # 주간 보상 안내
   st.info("💎 **주간 보상**: 매주 일요일 자정에 랭킹에 따라 보상이 지급됩니다. 상위 10%는 추가 보너스를 받습니다!")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
