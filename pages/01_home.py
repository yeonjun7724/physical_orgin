"""홈 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common import ProgressBar
from components.common.section_card import SectionCard, CloseSectionCard
from components.home import (
   GreetingCard, FeedItem, ActionButtonGrid, ResultSummaryCard
)
# 서비스는 필요할 때 service_cache에서 가져옴
from utils.constants import COLORS

# 공통 설정 적용
setup_common()


def _greeting_block():
   """인사말 블록"""
   user_name = st.session_state.get("user_name", "체력왕")
   GreetingCard(user_name)


def _hero_actions(go_to):
   """메인 액션 버튼들"""
   ActionButtonGrid([
      {
         "label": "💪 바로 측정하기",
         "key": "quick_measure",
         "type": "primary",
         "help": "종목을 선택하고 바로 측정을 시작합니다",
         "on_click": lambda: go_to("select_exercise")
      },
      {
         "label": "📊 목표 보기",
         "key": "view_goals",
         "type": "primary",
         "help": "나의 목표와 진행 상황을 확인합니다",
         "on_click": lambda: go_to("profile")
      }
   ])


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


def _recent_result_section():
   """최근 측정 결과 섹션"""
   from utils.page_utils import get_user_id
   from utils.service_cache import get_result_service
   user_id = get_user_id()
   if not user_id:
      ResultSummaryCard(
         score="0점",
         grade="5등급",
         percentile="0",
         metrics={"횟수": "0회", "정확도": "0%", "템포": "0s"}
      )
      return
   
   result_service = get_result_service()
   results = result_service.get_results_by_user(user_id)
   
   if results:
      # 최신 결과 가져오기
      latest_result = sorted(results, key=lambda x: x.get("created_at", ""), reverse=True)[0]
      score = latest_result.get("raw_score", 0)
      grade = latest_result.get("official_grade", "5등급")
      percentile = latest_result.get("percentile", 0)
      accuracy = latest_result.get("accuracy", 0)
      speed = latest_result.get("speed", 0)
      
      ResultSummaryCard(
         score=f"{score}점",
         grade=grade,
         percentile=str(percentile),
         metrics={
            "횟수": f"{score}회",
            "정확도": f"{int(accuracy * 100)}%",
            "템포": f"{speed/10:.1f}s"
         }
      )
   else:
      ResultSummaryCard(
         score="0점",
         grade="5등급",
         percentile="0",
         metrics={"횟수": "0회", "정확도": "0%", "템포": "0s"}
      )


def _feed_section():
   """피드 섹션 (라이트)"""
   SectionCard("🔥 최근 활동 피드")
   
   # 피드 아이템들
   feed_items = [
      {"name": "김철수", "exercise": "팔굽혀펴기", "score": "85점", "time": "2시간 전", "likes": 12},
      {"name": "이영희", "exercise": "윗몸일으키기", "score": "92점", "time": "5시간 전", "likes": 8},
      {"name": "박민수", "exercise": "스쿼트", "score": "78점", "time": "1일 전", "likes": 5},
   ]
   
   for item in feed_items:
      FeedItem(
         name=item['name'],
         exercise=item['exercise'],
         score=item['score'],
         time=item['time'],
         likes=item.get('likes', 0)
      )
   
   if st.button("더 보기", key="view_more_feed", use_container_width=True):
      st.info("더 많은 피드를 보려면 프로필 페이지를 확인하세요!")
   
   CloseSectionCard()


def render(go_to):
   """홈 페이지 렌더링"""
   _greeting_block()
   _hero_actions(go_to)
   _quests_section()
   _recent_result_section()
   _feed_section()


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)
