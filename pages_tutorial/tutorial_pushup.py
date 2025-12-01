"""팔굽혀펴기 튜토리얼 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common.section_card import section_card
from data.constants_exercise import EXERCISES

# 공통 설정 적용
setup_common()

def render(go_to):
    """팔굽혀펴기 튜토리얼 페이지 렌더링"""
    exercise_key = "pushup"
    info = EXERCISES[exercise_key]
    exercise_name = info["name"]
    
    # 운동 순서 정의
    exercise_order = ["pushup", "situp", "squat", "balance", "knee_lift", "trunk_flex"]
    current_index = exercise_order.index(exercise_key)
    prev_key = exercise_order[(current_index - 1) % len(exercise_order)]
    next_key = exercise_order[(current_index + 1) % len(exercise_order)]

    st.session_state.user_age = st.number_input("나이", 10, 80, 25)
    st.session_state.user_gender = st.selectbox("성별", ["남", "여"])    
    
    st.markdown("---")
    # 헤더 (이전 버튼 + 제목 + 다음 버튼)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("⬅️", key="prev_btn", help="이전 운동", use_container_width=True):
            go_to(f"tutorial_{prev_key}")
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{exercise_name} 튜토리얼</h2>", unsafe_allow_html=True)
    with col3:
        if st.button("➡️",  key="next_btn", help="다음 운동", use_container_width=True):
            go_to(f"tutorial_{next_key}")
    
    # 튜토리얼 설명
    st.markdown(f"<p style='text-align: center; color: #666;'>{info['tutorial_description']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 올바른 자세와 예시 영상 + 업로드 기능을 2열로 배치
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 올바른 자세 섹션
        with section_card("올바른 자세", icon="✅", variant="primary"):
            for idx, instruction in enumerate(info['instructions'], 1):
                col_num, col_text = st.columns([1, 10])
                with col_num:
                    st.markdown(f"**{idx}.**")
                with col_text:
                    st.markdown(instruction)
    
    with col_right:
        # 예시 영상 + 업로드 기능
        with section_card("예시 영상 및 업로드", icon="📹", variant="default"):
            st.info("올바른 자세는 아래 영상을 참고하거나 직접 영상을 업로드해 분석할 수 있습니다.")

            # 예시 영상 URL (원하면 추가)
            # st.video("https://your-example-video-url.mp4")

            # ⭐ 영상 업로드
            uploaded_file = st.file_uploader("팔굽혀펴기 영상 업로드", type=["mp4", "mov", "avi"])

            if uploaded_file is not None:
                st.success("영상이 업로드되었습니다.")
                st.video(uploaded_file)

                # 분석 버튼
                if st.button("영상 분석 시작", key="analyze_pushup", type="primary"):
                    st.session_state.uploaded_video = uploaded_file
                    st.session_state.selected_exercise = exercise_key
                    go_to("video_analysis_pushup")  # 분석 페이지로 이동
    
    # 기존 측정(실시간 카메라) 버튼 유지
    st.markdown("")  # 간격
    if st.button("측정 시작", key="start_measure", type="secondary", use_container_width=True):
        st.session_state.selected_exercise = exercise_key
        st.session_state.measure_started = True
        go_to("measure")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)
