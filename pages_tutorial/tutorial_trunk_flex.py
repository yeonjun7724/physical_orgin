"""상체 기울기 튜토리얼 페이지"""
import streamlit as st
from components.common.section_card import section_card
from data.constants_exercise import EXERCISES

def render(go_to):
    """상체 기울기 튜토리얼 페이지 렌더링"""
    exercise_key = "trunk_flex"
    info = EXERCISES[exercise_key]
    exercise_name = info["name"]
    
    # 운동 순서 정의
    exercise_order = ["pushup", "situp", "squat", "balance", "knee_lift", "trunk_flex"]
    current_index = exercise_order.index(exercise_key)
    prev_key = exercise_order[(current_index - 1) % len(exercise_order)]
    next_key = exercise_order[(current_index + 1) % len(exercise_order)]
    
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
    
    # 올바른 자세와 카메라 설정을 2열로 배치
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
            youtube_url = "https://www.youtube.com/embed/wVdOp3h1nog"
            st.markdown(f"""
                <iframe width="100%" height="350"
                src="{youtube_url}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
                </iframe>
            """, unsafe_allow_html=True)
            st.info("올바른 자세는 위 영상을 참고하세요")
            
    with col_right:
        # 카메라 설정 섹션
        with section_card("예시 영상 및 업로드", icon="📹", variant="default"):
            # ⭐ 영상 업로드
            uploaded_file = st.file_uploader(
                "상체 기울기 영상 업로드",
                type=["mp4", "mov", "avi"],
                key="trunk_flex_video_uploader"
            )

            if uploaded_file is not None:
                st.success("영상이 업로드되었습니다!")
                st.video(uploaded_file)
        
        # 분석 버튼 (section_card 밖으로 이동하여 col_right 전체 너비 사용)
        if uploaded_file is not None:
            if st.button("이 영상으로 자세 분석하기", type="primary", use_container_width=True, key="analyze_trunk_flex"):
                st.session_state.uploaded_video = uploaded_file
                st.session_state.selected_exercise = exercise_key

                # -------------------------
                # ⭐ 이동 경로 (중요!)
                # -------------------------
                go_to("video_analysis_trunk_flex")
        else:
            st.button("이 영상으로 자세 분석하기", type="secondary", use_container_width=True, key="analyze_trunk_flex", disabled=True)


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__":
    from utils.page_utils import run_page
    run_page(render)

