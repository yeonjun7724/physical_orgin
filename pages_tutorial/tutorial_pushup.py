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

    st.markdown("---")

    # ---------------------------------------
    # 상단 사용자 정보 입력
    # ---------------------------------------
    st.subheader("사용자 정보")

    col_age, col_gender = st.columns(2)
    with col_age:
        st.session_state.user_age = st.number_input("나이", min_value=10, max_value=80, value=25)
    with col_gender:
        st.session_state.user_gender = st.selectbox("성별", ["남", "여"])
    
    st.markdown("---")

    # 헤더 (이전 / 제목 / 다음)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("⬅️", key="prev_btn", help="이전 운동", use_container_width=True):
            go_to(f"tutorial_{prev_key}")
    with col2:
        st.markdown(
            f"<h2 style='text-align: center;'>{exercise_name} 튜토리얼</h2>",
            unsafe_allow_html=True,
        )
    with col3:
        if st.button("➡️", key="next_btn", help="다음 운동", use_container_width=True):
            go_to(f"tutorial_{next_key}")
    
    # 설명
    st.markdown(
        f"<p style='text-align: center; color: #666;'>{info['tutorial_description']}</p>",
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    # ---------------------------------------
    # 2컬럼 (왼: 자세 / 오른: 예시 영상 + 업로드)
    # ---------------------------------------
    col_left, col_right = st.columns(2)
    
    # -------------------------
    # 왼쪽: 올바른 자세
    # -------------------------
    with col_left:
        with section_card("올바른 자세", icon="✅", variant="primary"):
            for idx, instruction in enumerate(info['instructions'], 1):
                col_num, col_text = st.columns([1, 10])
                with col_num:
                    st.markdown(f"**{idx}.**")
                with col_text:
                    st.markdown(instruction)
    
    # -------------------------
    # 오른쪽: 예시 + 업로드
    # -------------------------
    with col_right:
        with section_card("예시 영상 및 업로드", icon="📹", variant="default"):
            st.info("올바른 자세는 아래 영상을 참고하거나, 직접 촬영한 영상을 업로드해 분석할 수 있습니다.")

            # ⭐ 영상 업로드
            uploaded_file = st.file_uploader(
                "팔굽혀펴기 영상 업로드",
                type=["mp4", "mov", "avi"],
                key="pushup_video_uploader"
            )

            if uploaded_file is not None:
                st.success("영상이 업로드되었습니다!")
                st.video(uploaded_file)

                # 분석 버튼
                if st.button("이 영상으로 자세 분석하기", type="primary", use_container_width=True):
                    st.session_state.uploaded_video = uploaded_file
                    st.session_state.selected_exercise = exercise_key

                    # -------------------------
                    # ⭐ 이동 경로 (중요!)
                    # -------------------------
                    go_to("video_analysis_pushup")
    
    # ---------------------------------------
    # 기존 실시간 측정 기능 버튼
    # ---------------------------------------
    st.markdown("")
    if st.button("실시간 측정 시작", key="start_measure", type="secondary", use_container_width=True):
        st.session_state.selected_exercise = exercise_key
        st.session_state.measure_started = True
        go_to("measure")


# 페이지 직접 실행
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)
