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
        st.markdown("# 💪 체력 FIT")
        st.markdown("#### 로그인하여 서비스를 이용하세요")
        st.markdown("---")
        
        # 사용자명 입력 (이메일 또는 사용자명)
        identifier = st.text_input(
            "이메일 또는 사용자명",
            placeholder="example@email.com 또는 사용자명",
            key="login_identifier"
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
            if not identifier or not password:
                st.error("이메일(또는 사용자명)과 비밀번호를 모두 입력하세요.")
            else:
                success, message = login_user(identifier, password)
                if success:
                    st.success("로그인 성공!")
                    # 홈 페이지로 이동
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error(message)

        # 회원가입 페이지로 이동
        st.markdown("---")
        st.markdown("계정이 없으신가요?")
        if st.button("회원가입하기", use_container_width=True, key="go_to_signup"):
            st.session_state.page = "signup"
            st.rerun()


def render(go_to=None):
    """로그인 페이지 렌더링 (routes.py 호환)"""
    render_login_page()


def logout():
    """로그아웃 처리"""
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.user_id = None
    st.rerun()
