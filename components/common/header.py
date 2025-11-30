import streamlit as st
from utils.auth import is_authenticated, get_current_user

def render_header():

    # --------------------------
    # 로고 + 구분선 CSS
    # --------------------------
    st.markdown("""
    <style>
    .app-header-box {
        padding: 12px 20px 6px 20px;
        background: #ffffff;
        border-bottom: 2px solid #4c84af;
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 6px;
    }
    .app-logo {
        font-size: 22px;
        font-weight: 800;
        color: #4c84af;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------
    # 로고 행 (맨 위)
    # --------------------------
    st.markdown('<div class="app-header-box"><div class="app-logo">💪 체력왕 FIT</div></div>', unsafe_allow_html=True)

    # --------------------------
    # 네비 버튼 + 사용자 + 로그아웃 한 줄(Row)
    # --------------------------

    # 버튼 너비 고정 및 간격 조정 (버튼 길이가 달라져도 동일한 크기)
    button_style = """
    <style>
    div[data-testid="stHorizontalBlock"] button {
        width: 110px !important;
        margin-right: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        gap: 8px !important;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # 전체 헤더 행
    col_intro, col_home, col_rank, col_prof, col_store, col_set, col_user = st.columns(
        [1, 1, 1, 1, 1, 1, 2]
    )

    current = st.session_state.get("page", "home")

    # 헬퍼
    def go(page):
        st.session_state.page = page
        st.rerun()

    # --------------------------
    # 페이지 버튼들 (가로 너비 동일)
    # --------------------------
    with col_intro:
        if st.button("소개", type=("primary" if current == "introduction" else "secondary"), key="nav_intro"):
            go("introduction")

    with col_home:
        if st.button("홈", type=("primary" if current == "home" else "secondary"), key="nav_home"):
            go("home")

    with col_rank:
        if st.button("랭킹", type=("primary" if current == "ranking" else "secondary"), key="nav_rank"):
            go("ranking")

    with col_prof:
        if st.button("프로필", type=("primary" if current == "profile" else "secondary"), key="nav_profile"):
            go("profile")

    with col_store:
        if st.button("상점", type=("primary" if current == "store" else "secondary"), key="nav_store"):
            go("store")

    with col_set:
        if st.button("설정", type=("primary" if current == "setting" else "secondary"), key="nav_setting"):
            go("setting")

    # --------------------------
    # 사용자 이름 + logout (한 줄, 오른쪽 정렬)
    # --------------------------
    with col_user:
        if is_authenticated():
            if st.button("로그아웃", key="logout_btn"):
                from pages_auth.login import logout
                logout()
        else:
            st.markdown("로그인 필요")