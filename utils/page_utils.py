"""페이지 관련 유틸리티 함수"""
import streamlit as st
from functools import wraps


def require_auth(func):
    """인증이 필요한 페이지를 위한 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = st.session_state.get("user_id")
        if not user_id:
            st.warning("로그인이 필요합니다.")
            return
        return func(*args, **kwargs)
    return wrapper


def get_user_id():
    """현재 사용자 ID를 가져오는 헬퍼 함수"""
    return st.session_state.get("user_id")


def run_page(render_func):
    """페이지 실행 패턴을 통일하는 헬퍼 함수
    
    사용 예시:
        if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
            from utils.routes import go_to
            run_page(lambda: render(go_to))
    """
    from utils.routes import go_to
    render_func(go_to)

