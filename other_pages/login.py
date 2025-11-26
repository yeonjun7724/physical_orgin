"""로그인 컴포넌트"""
import streamlit as st
from utils.auth import login_user


def render_login_page():
    """로그인 페이지 렌더링"""
    # 사이드바 숨기기 (필수 CSS만 유지)
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none !important; }
        section[data-testid="stMain"] { margin-left: 0 !important; }
        button[data-testid="baseButton-header"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 중앙 정렬을 위한 컬럼 사용
    col1, col2, col3 = st.columns([1, 4, 1], gap="large")
    
    with col2:
        # 제목
        st.markdown("# 💪 체력왕 FIT")
        st.markdown("#### 로그인하여 서비스를 이용하세요")
        st.markdown("---")
        
        # 사용자명 입력
        username = st.text_input(
            "사용자명",
            placeholder="사용자명을 입력하세요",
            key="login_username"
        )
        
        # 비밀번호 입력
        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호를 입력하세요",
            key="login_password"
        )
        
        # 로그인 버튼
        if st.button("로그인", type="primary", use_container_width=True, key="login_btn"):
            # 검증 없이 바로 로그인 처리
            if username:
                login_user(username)
                st.rerun()
            else:
                # 사용자명이 없으면 기본값 사용
                login_user("체력왕")
                st.rerun()
        
        # 회원가입 페이지로 이동
        st.markdown("---")
        st.markdown("계정이 없으신가요?")
        if st.button("회원가입하기", use_container_width=True, key="go_to_signup"):
            st.session_state.page = "signup"
            st.rerun()


def logout():
    """로그아웃 처리"""
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.user_id = None
    st.rerun()
