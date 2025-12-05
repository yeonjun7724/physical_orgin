"""인증 핸들러 - 로그인 체크 및 페이지 표시"""
import streamlit as st
from utils.auth import is_authenticated
import utils.style as style


def check_auth_and_show_login():
    """인증 체크 후 로그인되지 않았으면 로그인 페이지 표시"""
    # 순환 import 방지를 위해 함수 내부에서 import
    from pages_auth.login import render_login_page
    from pages_auth.signup import render_signup_page
    
    # signup과 login 페이지는 인증 없이 접근 가능
    current_page = st.session_state.get("page", "home")
    if current_page == "signup":

        style.apply_global_css()
        render_signup_page()
        st.stop()
        return
    
    if current_page == "login":
        # 로그인된 사용자가 login 페이지에 접근하면 홈으로 리다이렉트
        if is_authenticated():
            st.session_state.page = "home"
            st.rerun()
            return
        
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
        
        render_login_page()
        st.stop()
        return
    
    if not is_authenticated():
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

