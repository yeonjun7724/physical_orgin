"""운동 종목 선택 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.exercise.exercise_card import ExerciseItemCard
from components.common import PageHeader
from utils.constants import EXERCISES

# 공통 설정 적용
setup_common()


def _create_exercise_handler(exercise_key, go_to):
   """운동 시작 핸들러 생성 (중복 제거)"""
   def handler():
      st.session_state.selected_exercise = exercise_key
      go_to(f"tutorial_{exercise_key}")
   return handler


def render(go_to):
   """종목 선택 페이지 렌더링"""
   PageHeader("운동 종목 선택", "측정하고 싶은 종목을 선택하세요. 6종목 모두 측정 시 약 10분 소요됩니다.", "🏋️")
   
   # 전체 측정 안내
   st.info("💡 **팁**: 6종목을 모두 측정하면 종합 등급을 받을 수 있습니다!")
   
   # 운동 리스트 생성 (constants에서 가져오기)
   exercises_list = list(EXERCISES.values())
   
   # 2열 그리드로 배치
   for i in range(0, len(exercises_list), 2):
      col1, col2 = st.columns(2)
      
      with col1:
         ExerciseItemCard(
            name=exercises_list[i]["name"],
            description=exercises_list[i]["description"],
            duration_label=exercises_list[i]["duration_label"],
            difficulty_label=exercises_list[i]["difficulty_label"],
            icon=exercises_list[i]["icon"],
            key=exercises_list[i]["key"],
            on_start=_create_exercise_handler(exercises_list[i]["key"], go_to),
         )
      
      with col2:
         if i + 1 < len(exercises_list):
            ExerciseItemCard(
               name=exercises_list[i + 1]["name"],
               description=exercises_list[i + 1]["description"],
               duration_label=exercises_list[i + 1]["duration_label"],
               difficulty_label=exercises_list[i + 1]["difficulty_label"],
               icon=exercises_list[i + 1]["icon"],
               key=exercises_list[i + 1]["key"],
               on_start=_create_exercise_handler(exercises_list[i + 1]["key"], go_to),
            )
   
   # 전체 측정 버튼
   if st.button("🚀 6종목 전체 측정 시작 (약 10분)", key="all_exercises", use_container_width=True, type="primary"):
      st.session_state.selected_exercise = "전체 측정"
      go_to("tutorial_pushup")  # 첫 번째 운동으로 시작


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
   from utils.page_utils import run_page
   run_page(render)