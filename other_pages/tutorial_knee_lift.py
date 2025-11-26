"""제자리 무릎들기 튜토리얼 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common.section_card import section_card
from utils.constants import EXERCISES

# 공통 설정 적용
setup_common()

def render(go_to):
    """제자리 무릎들기 튜토리얼 페이지 렌더링"""
    exercise_name = "제자리 무릎들기"
    info = EXERCISES[exercise_name]
    
    # 헤더 (뒤로가기 버튼 + 제목)
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("←", key="back_btn", help="뒤로가기"):
            go_to("select_exercise")
    with col2:
        st.markdown(f"## {exercise_name} 튜토리얼")
    
    # 운동 설명 카드
    col_icon, col_info = st.columns([1, 4])
    with col_icon:
        st.markdown(f"### {info['icon']}")
    with col_info:
        st.markdown(f"### {exercise_name}")
        st.caption(info['tutorial_description'])
    
    st.markdown("---")
    
    # 올바른 자세 섹션
    with section_card("올바른 자세", icon="▶", variant="primary"):
        for idx, instruction in enumerate(info['instructions'], 1):
            col_num, col_text = st.columns([1, 10])
            with col_num:
                st.markdown(f"**{idx}.**")
            with col_text:
                st.markdown(instruction)
    
    # 카메라 설정 섹션
    with section_card("카메라 설정", icon="📷", variant="default"):
        # 카메라 미리보기 영역
        st.markdown("### 📹 카메라 미리보기")
        st.info("카메라 권한을 허용하면 여기에 미리보기가 표시됩니다.")
        
        # 카메라 권한 및 시작 버튼
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("카메라 권한 허용", key="camera_permission", use_container_width=True):
                st.info("카메라 권한이 허용되었습니다.")
        
        with col2:
            if st.button("측정 시작", key="start_measure", type="primary", use_container_width=True):
                st.session_state.selected_exercise = exercise_name
                st.session_state.measure_started = True
                go_to("measure")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

