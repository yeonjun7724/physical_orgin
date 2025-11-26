"""인증 핸들러 - 로그인 체크 및 페이지 표시"""
import streamlit as st
from utils.auth import is_authenticated
from other_pages.login import render_login_page
from other_pages.signup import render_signup_page
from utils.routes import render_page
import utils.style as style


def check_auth_and_show_login():
    """인증 체크 후 로그인되지 않았으면 로그인 페이지 표시"""
    # signup 페이지는 인증 없이 접근 가능
    current_page = st.session_state.get("page", "home")
    if current_page == "signup":
        # signup 페이지는 별도 처리
        st.set_page_config(
            page_title="체력왕 FIT - 회원가입",
            page_icon="💪",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        style.apply_global_css()
        render_signup_page()
        st.stop()
        return
    
    if not is_authenticated():
        # 페이지 설정
        st.set_page_config(
            page_title="체력왕 FIT - 로그인",
            page_icon="💪",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        
        # 전역 스타일 적용
        style.apply_global_css()
        
        # 사이드바 완전히 숨기기
        st.markdown(
            """
            <style>
            /* 사이드바 완전히 숨기기 */
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            
            /* 메인 콘텐츠 영역 확장 */
            section[data-testid="stMain"] {
                margin-left: 0 !important;
            }
            
            /* 사이드바 토글 버튼 숨기기 */
            button[data-testid="baseButton-header"] {
                display: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # 로그인 페이지 표시
        render_login_page()
        st.stop()

