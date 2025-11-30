"""랭킹 페이지"""
import streamlit as st
import pandas as pd
from utils.app_common import setup_common
from components.common.section_card import SectionCard, CloseSectionCard
from components.cards.rank_card import MyRankCard, RankCard
# 서비스는 필요할 때 service_cache에서 가져옴
from data.constants_exercise import EXERCISES
from data.constants import COLORS

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
      "종합": "종합",
      "pushup": "팔굽혀펴기",
      "situp": "윗몸일으키기",
      "squat": "스쿼트 리듬",
      "balance": "외발서기",
      "kneelift": "제자리 무릎들기",
      "trunkFlex": "상체 기울기"
   }
   
   # 현재 선택된 운동 종목 (기본값: "종합")
   if "ranking_event" not in st.session_state:
      st.session_state.ranking_event = "종합"
   
   # 버튼 크기 통일을 위한 CSS
   st.markdown(
      """
      <style>
      div[data-testid*="event_btn_"] button {
         min-width: 130px !important;
         min-height: 100px !important;
         height: 100px !important;
         width: 100% !important;
      }
      /* 선택된 버튼(primary) 파란색 계열로 변경 */
      div[data-testid*="event_btn_"] button[kind="primary"] {
         background-color: #4c84af !important;
         color: white !important;
         border-color: #4c84af !important;
      }
      div[data-testid*="event_btn_"] button[kind="primary"]:hover {
         background-color: #3a6a8a !important;
         border-color: #3a6a8a !important;
      }
      /* 선택되지 않은 버튼(secondary) 스타일 */
      div[data-testid*="event_btn_"] button[kind="secondary"] {
         background-color: #f0f0f0 !important;
         color: #333 !important;
         border-color: #ddd !important;
      }
      div[data-testid*="event_btn_"] button[kind="secondary"]:hover {
         background-color: #e0e0e0 !important;
         border-color: #ccc !important;
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
   
   # 사용자 프로필에서 나이대 가져오기
   user_profile = profile_service.get_profile_by_user_id(user_id)
   user_age_group = user_profile.get("age_group", "성인기") if user_profile else "성인기"
   
   # 기간 선택
   if "ranking_period" not in st.session_state:
      st.session_state.ranking_period = "주간"
   period_options = ["주간", "월간", "연간"]
   period_index = period_options.index(st.session_state.ranking_period) if st.session_state.ranking_period in period_options else 0
   period = st.selectbox(
      "기간",
      period_options,
      index=period_index,
      help="기간별 랭킹을 확인할 수 있습니다",
      key="ranking_period_selectbox"
   )
   # 기간이 변경되면 세션 상태 업데이트 및 리렌더링
   if st.session_state.ranking_period != period:
      st.session_state.ranking_period = period
      st.rerun()
   
   # 사용자 나이대 표시
   st.info(f"📊 나이대별 랭킹이 표시됩니다 :현재 만**{user_age_group}**세")
   
   CloseSectionCard()
   
   # 내 순위 카드
   my_rank = None
   my_score = 0
   # LEADERBOARD_SAMPLE에서 데이터 가져오기
   from data.constants_exercise import LEADERBOARD_SAMPLE
   
   # 기간 매핑
   period_mapping = {
      "주간": "weekly",
      "월간": "monthly",
      "연간": "season"
   }
   period_key = period_mapping.get(period, "weekly")
   
   # 이벤트 키 매핑 (종합 -> overall)
   event_key_mapping = {
      "종합": "overall",
      "pushup": "pushup",
      "situp": "situp",
      "squat": "squat",
      "balance": "balance",
      "kneelift": "knee_lift",
      "trunkFlex": "trunk_flex"
   }
   event_key = event_key_mapping.get(event, event)
   
   # LEADERBOARD_SAMPLE에서 데이터 가져오기
   leaderboard = []
   if event_key in LEADERBOARD_SAMPLE and period_key in LEADERBOARD_SAMPLE[event_key]:
      leaderboard = LEADERBOARD_SAMPLE[event_key][period_key].copy()
   
   # 나이대 필터링 적용 (LEADERBOARD_SAMPLE에는 나이대 정보가 없으므로 일단 스킵)
   # TODO: 나이대 정보가 추가되면 사용자 나이대로 필터링
   
   # 점수 순으로 정렬
   leaderboard = sorted(leaderboard, key=lambda x: x.get("score", 0), reverse=True)
   
   # 내 순위 찾기
   for idx, entry in enumerate(leaderboard):
      if entry.get("user_id") == user_id:
         my_rank = entry.copy()
         my_rank["rank"] = idx + 1
         break
   
   if my_rank:
      my_score = my_rank.get("score", 0)
      rank = my_rank.get("rank", 0)
   else:
      # LEADERBOARD_SAMPLE에 사용자 데이터가 없는 경우 실제 결과 데이터에서 계산
      rank = 0
      my_score = 0
      
      if event == "종합":
         # 종합일 때는 평균 점수 계산
         all_results = result_service.get_results_by_user(user_id)
         if all_results:
            my_score = int(sum(r.get("raw_score", 0) for r in all_results) / len(all_results))
            # 내 점수보다 높은 사람 수를 세어서 순위 계산
            rank = sum(1 for entry in leaderboard if entry.get("score", 0) > my_score) + 1
      else:
         # 특정 종목일 때는 해당 종목의 최신 점수 사용
         event_results = [
            r for r in result_service.get_results_by_user(user_id)
            if r.get("event", "").lower() == event.lower() or 
               (event == "kneelift" and r.get("event", "") in ["kneelift", "knee_lift"]) or
               (event == "trunkFlex" and r.get("event", "") in ["trunkFlex", "trunk_flex"])
         ]
         if event_results:
            # 최신 결과의 점수 사용
            latest_result = sorted(event_results, key=lambda x: x.get("created_at", ""), reverse=True)[0]
            my_score = latest_result.get("raw_score", 0)
            # 내 점수보다 높은 사람 수를 세어서 순위 계산
            rank = sum(1 for entry in leaderboard if entry.get("score", 0) > my_score) + 1
   
   # 등급 계산
   from data.constants_exercise import GRADE_INFO
   grade = "5등급"
   for grade_name, grade_info in sorted(GRADE_INFO.items(), key=lambda x: x[1]["min"], reverse=True):
      if my_score >= grade_info["min"]:
         grade = grade_name
         break
   
   # 퍼센타일 계산 (랭킹에 있는 경우)
   percentile = "0"
   if leaderboard and rank > 0:
      total_entries = len(leaderboard)
      percentile = str(int((total_entries - rank + 1) / total_entries * 100)) if total_entries > 0 else "0"
   
   # 랭킹에 등록되지 않은 경우 처리
   display_rank = rank if rank > 0 else 999  # 랭킹에 없으면 999위로 표시
   reward_text = f"{period} 보상: +{min(200, max(50, 250 - rank * 10))} FIT" if rank > 0 else "랭킹에 등록되지 않았습니다"
   
   MyRankCard(
      rank=display_rank,
      percentile=percentile,
      total_score=my_score,
      grade=grade,
      reward=reward_text
   )
   # 주간 보상 안내
   st.info("💎 **주간 보상**: 매주 일요일 자정에 랭킹에 따라 보상이 지급됩니다. 상위 10%는 추가 보너스를 받습니다!")

   # 랭킹 테이블
   SectionCard("📊 랭킹 목록")
   
   # LEADERBOARD_SAMPLE에서 데이터 가져오기
   from data.constants_exercise import LEADERBOARD_SAMPLE
   
   # 기간 매핑: "주간" -> "weekly", "월간" -> "monthly", "연간" -> "season"
   period_mapping = {
      "주간": "weekly",
      "월간": "monthly",
      "연간": "season"
   }
   period_key = period_mapping.get(period, "weekly")
   
   # 이벤트 키 매핑 (종합 -> overall, kneelift -> knee_lift, trunkFlex -> trunk_flex)
   event_key_mapping = {
      "종합": "overall",
      "pushup": "pushup",
      "situp": "situp",
      "squat": "squat",
      "balance": "balance",
      "kneelift": "knee_lift",
      "trunkFlex": "trunk_flex"
   }
   event_key = event_key_mapping.get(event, event)
   
   # LEADERBOARD_SAMPLE에서 데이터 가져오기
   leaderboard = []
   if event_key in LEADERBOARD_SAMPLE and period_key in LEADERBOARD_SAMPLE[event_key]:
      leaderboard = LEADERBOARD_SAMPLE[event_key][period_key].copy()
   
   
   # 점수 순으로 정렬 (이미 정렬되어 있지만 확실히 하기 위해)
   leaderboard = sorted(leaderboard, key=lambda x: x.get("score", 0), reverse=True)
   
   # 상위 20개만 표시 
   limit = 20
   leaderboard = leaderboard[:limit]
   
   if leaderboard:
      # 프로필 정보 가져오기
      ranking_data = []
      for idx, entry in enumerate(leaderboard):
         # 순위는 인덱스 기반으로 재계산
         rank = idx + 1
         
         # LEADERBOARD_SAMPLE에는 nickname이 이미 포함되어 있음
         nickname = entry.get("nickname", "알 수 없음")
         
         ranking_data.append({
            "순위": rank,
            "닉네임": nickname,
            "총점": entry.get("score", 0),
            "등급": "1등급",  # TODO: 등급 계산
            "연령대": entry.get("age_group", "-"),  # LEADERBOARD_SAMPLE에는 나이대 정보가 없음
            "성별": "남성" if entry.get("gender") == "M" else ("여성" if entry.get("gender") == "F" else "-"),
         })
      
      df = pd.DataFrame(ranking_data)
      
      # 상위 3명 특별 표시
      top3 = leaderboard[:3]
      top3_cols = st.columns(3)
      for idx, entry in enumerate(top3):
         with top3_cols[idx]:
            # LEADERBOARD_SAMPLE에는 nickname이 이미 포함되어 있음
            name = entry.get("nickname", "알 수 없음")
            
            RankCard(
               rank=idx + 1,  # 순위는 인덱스 기반
               name=name,
               score=f"{entry.get('score', 0)}점"
            )
      
      # 상위 3명 카드와 랭킹 표 사이 간격
      st.markdown("<br><br>", unsafe_allow_html=True)
      
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
   
   CloseSectionCard()
   


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
