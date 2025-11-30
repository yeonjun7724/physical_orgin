"""측정 페이지"""
import streamlit as st
from utils.app_common import setup_common

# 공통 설정 적용
setup_common()


def render(go_to):
    """측정 페이지 렌더링"""
    from utils.page_utils import get_user_id
    user_id = get_user_id()
    if not user_id:
        st.warning("로그인이 필요합니다.")
        return
    
    selected_exercise = st.session_state.get("selected_exercise", "")
    
    if not selected_exercise:
        st.warning("측정할 운동을 선택해주세요.")
        st.button("홈으로 돌아가기", on_click=lambda: go_to("home"))
        return
    
    st.title("측정 중...")
    st.info("측정 기능은 준비 중입니다.")
    
    if st.button("홈으로 돌아가기"):
        go_to("home")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

