"""결과 페이지"""
import streamlit as st

def render(go_to):
    """결과 페이지 렌더링"""
    from utils.page_utils import get_user_id
    user_id = get_user_id()
    if not user_id:
        st.warning("로그인이 필요합니다.")
        return
    
    st.title("측정 결과")
    st.info("결과 페이지는 준비 중입니다.")
    
    if st.button("홈으로 돌아가기"):
        go_to("home")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

