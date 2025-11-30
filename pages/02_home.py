"""홈 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common import ProgressBar
from components.common.section_card import SectionCard, CloseSectionCard
from components.cards.home_card import (
   GreetingCard, FeedItem, ResultSummaryCard
)
from components.cards.exercise_card import ExerciseItemCard
# 서비스는 필요할 때 service_cache에서 가져옴
from data.constants_exercise import COLORS, EXERCISES

# 공통 설정 적용
setup_common()


def _greeting_block():
   """인사말 블록"""
   user_name = st.session_state.get("user_name", "체력왕")
   GreetingCard(user_name, scroll_target_id="exercise-selection")


def _quests_section():
   """퀘스트 섹션"""
   from utils.page_utils import get_user_id
   from utils.service_cache import get_result_service, get_streak_service
   user_id = get_user_id()
   if not user_id:
      return
   
   result_service = get_result_service()
   streak_service = get_streak_service()
   
   # 오늘의 측정 횟수 계산
   from datetime import datetime, date
   today = date.today().isoformat()
   today_results = [
      r for r in result_service.get_results_by_user(user_id)
      if r.get("created_at", "").startswith(today)
   ]
   today_count = len(today_results)
   
   # 연속 측정 일수
   streak = streak_service.get_user_streak(user_id)
   current_streak = streak.get("current_streak", 0) if streak else 0
   
   SectionCard("📋 오늘의 퀘스트")
   
   ProgressBar("오늘의 측정", current=today_count, total=3, reward_label="+100 FIT")
   st.markdown("")  # 간격
   ProgressBar("주간 챌린지", current=6, total=10, reward_label="+500 FIT")
   st.markdown("")  # 간격
   ProgressBar("연속 측정", current=current_streak, total=7, reward_label="뱃지 획득")
   
   CloseSectionCard()


def _format_time_ago(date_str: str) -> str:
   """날짜 문자열을 '2주 전', '5달 전' 형식으로 변환"""
   from datetime import datetime, timezone
   
   try:
      # ISO 형식 파싱
      if "T" in date_str:
         if date_str.endswith("Z"):
            created_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
         else:
            created_date = datetime.fromisoformat(date_str)
      else:
         created_date = datetime.fromisoformat(date_str)
      
      # UTC 시간을 로컬 시간으로 변환 (필요시)
      if created_date.tzinfo:
         now = datetime.now(timezone.utc)
      else:
         now = datetime.now()
         created_date = created_date.replace(tzinfo=None)
      
      # 날짜 차이 계산
      if created_date.tzinfo:
         diff = now - created_date
      else:
         diff = now.replace(tzinfo=None) - created_date
      
      days = diff.days
      weeks = days // 7
      months = days // 30
      years = days // 365
      
      if years > 0:
         return f"{years}년 전"
      elif months > 0:
         return f"{months}달 전"
      elif weeks > 0:
         return f"{weeks}주 전"
      elif days > 0:
         return f"{days}일 전"
      else:
         hours = diff.seconds // 3600
         if hours > 0:
            return f"{hours}시간 전"
         else:
            minutes = diff.seconds // 60
            return f"{minutes}분 전" if minutes > 0 else "방금 전"
   except:
      return "알 수 없음"


def _recent_result_section():
   """최근 측정 결과 섹션 - 6개 종목별로 표시"""
   from utils.page_utils import get_user_id
   from utils.service_cache import get_result_service
   from datetime import datetime
   
   user_id = get_user_id()
   
   # 이벤트 키 매핑 (result의 event -> EXERCISES의 name)
   event_key_mapping = {
      "pushup": "팔굽혀펴기",
      "situp": "윗몸일으키기",
      "squat": "스쿼트 리듬",
      "balance": "외발서기",
      "kneelift": "제자리 무릎들기",
      "knee_lift": "제자리 무릎들기",
      "trunkFlex": "상체 기울기",
      "trunk_flex": "상체 기울기"
   }
   
   # 모든 종목 목록
   all_exercises = {
      "pushup": "팔굽혀펴기",
      "situp": "윗몸일으키기",
      "squat": "스쿼트 리듬",
      "balance": "외발서기",
      "knee_lift": "제자리 무릎들기",
      "trunk_flex": "상체 기울기"
   }
   
   SectionCard("📊 최근 측정 결과")
   
   # 종목 리스트를 리스트로 변환 (순서 보장)
   exercises_list = list(all_exercises.items())
   
   if not user_id:
      # 로그인 안 된 경우 - 2열 3행으로 배치
      for i in range(0, len(exercises_list), 2):
         col1, col2 = st.columns(2)
         
         with col1:
            exercise_key, exercise_name = exercises_list[i]
            st.markdown(
               f"""
               <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                           border-left: 4px solid #ddd;">
                  <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                  <div style="font-size: 0.9rem; color: #999;">측정 기록 없음</div>
                  <div style="font-size: 0.9rem; color: #999;">-</div>
               </div>
               """,
               unsafe_allow_html=True
            )
         
         with col2:
            if i + 1 < len(exercises_list):
               exercise_key, exercise_name = exercises_list[i + 1]
               st.markdown(
                  f"""
                  <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                              border-left: 4px solid #ddd;">
                     <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                     <div style="font-size: 0.9rem; color: #999;">측정 기록 없음</div>
                     <div style="font-size: 0.9rem; color: #999;">-</div>
                  </div>
                  """,
                  unsafe_allow_html=True
               )
   else:
      result_service = get_result_service()
      results = result_service.get_results_by_user(user_id)
      
      # 종목별로 최신 결과 찾기
      exercise_results = {}
      for result in results:
         event = result.get("event", "")
         # 이벤트 키 정규화 (kneelift -> knee_lift, trunkFlex -> trunk_flex)
         if event == "kneelift":
            event = "knee_lift"
         elif event == "trunkFlex":
            event = "trunk_flex"
         
         if event in all_exercises:
            # 이미 해당 종목의 결과가 없거나, 더 최신 결과인 경우
            if event not in exercise_results:
               exercise_results[event] = result
            else:
               existing_date = exercise_results[event].get("created_at", "")
               current_date = result.get("created_at", "")
               if current_date > existing_date:
                  exercise_results[event] = result
      
      # 2열 3행으로 배치
      for i in range(0, len(exercises_list), 2):
         col1, col2 = st.columns(2)
         
         with col1:
            exercise_key, exercise_name = exercises_list[i]
            if exercise_key in exercise_results:
               result = exercise_results[exercise_key]
               created_at = result.get("created_at", "")
               percentile = result.get("percentile", 0)
               time_ago = _format_time_ago(created_at)
               
               st.markdown(
                  f"""
                  <div style="background: #f0f7ff; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                              border-left: 4px solid #4c84af;">
                     <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                     <div style="font-size: 0.95rem; color: #666; margin-bottom: 0.25rem;">{time_ago}</div>
                     <div style="font-size: 0.95rem; color: #4c84af; font-weight: 600;">상위 {percentile}%</div>
                  </div>
                  """,
                  unsafe_allow_html=True
               )
            else:
               # 측정 기록이 없는 종목
               st.markdown(
                  f"""
                  <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                              border-left: 4px solid #ddd;">
                     <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                     <div style="font-size: 0.9rem; color: #999;">측정 기록 없음</div>
                     <div style="font-size: 0.9rem; color: #999;">-</div>
                  </div>
                  """,
                  unsafe_allow_html=True
               )
         
         with col2:
            if i + 1 < len(exercises_list):
               exercise_key, exercise_name = exercises_list[i + 1]
               if exercise_key in exercise_results:
                  result = exercise_results[exercise_key]
                  created_at = result.get("created_at", "")
                  percentile = result.get("percentile", 0)
                  time_ago = _format_time_ago(created_at)
                  
                  st.markdown(
                     f"""
                     <div style="background: #f0f7ff; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                                 border-left: 4px solid #4c84af;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                        <div style="font-size: 0.95rem; color: #666; margin-bottom: 0.25rem;">{time_ago}</div>
                        <div style="font-size: 0.95rem; color: #4c84af; font-weight: 600;">상위 {percentile}%</div>
                     </div>
                     """,
                     unsafe_allow_html=True
                  )
               else:
                  # 측정 기록이 없는 종목
                  st.markdown(
                     f"""
                     <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                                 border-left: 4px solid #ddd;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">{exercise_name}</div>
                        <div style="font-size: 0.9rem; color: #999;">측정 기록 없음</div>
                        <div style="font-size: 0.9rem; color: #999;">-</div>
                     </div>
                     """,
                     unsafe_allow_html=True
                  )
   
   CloseSectionCard()


def _create_exercise_handler(exercise_key, go_to):
   """운동 시작 핸들러 생성 (중복 제거)"""
   def handler():
      st.session_state.selected_exercise = exercise_key
      go_to(f"tutorial_{exercise_key}")
   return handler


def _exercise_selection_section(go_to):
   """운동 종목 선택 섹션"""
   # 스크롤 타겟을 위한 마커
   st.markdown('<div id="exercise-selection"></div>', unsafe_allow_html=True)
   SectionCard("💪 운동 종목 선택")

   # 운동 리스트 생성 (키와 값을 함께 가져오기)
   exercises_items = list(EXERCISES.items())
   
   # 2열 그리드로 배치
   for i in range(0, len(exercises_items), 2):
      col1, col2 = st.columns(2)
      
      with col1:
         exercise_key, exercise_data = exercises_items[i]
         ExerciseItemCard(
            name=exercise_data["name"],
            description=exercise_data["description"],
            duration_label=exercise_data["duration_label"],
            difficulty_label=exercise_data["difficulty_label"],
            icon=exercise_data["icon"],
            key=exercise_key,
            on_start=_create_exercise_handler(exercise_key, go_to),
         )
      
      with col2:
         if i + 1 < len(exercises_items):
            exercise_key, exercise_data = exercises_items[i + 1]
            ExerciseItemCard(
               name=exercise_data["name"],
               description=exercise_data["description"],
               duration_label=exercise_data["duration_label"],
               difficulty_label=exercise_data["difficulty_label"],
               icon=exercise_data["icon"],
               key=exercise_key,
               on_start=_create_exercise_handler(exercise_key, go_to),
            )
   
   CloseSectionCard()



def render(go_to):
   """홈 페이지 렌더링"""
   _greeting_block()
   
   # 오늘의 퀘스트와 최근 측정 결과를 2열로 배치
   col1, col2 = st.columns(2)
   
   with col1:
      _quests_section()
   
   with col2:
      _recent_result_section()
   
   _exercise_selection_section(go_to)


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
