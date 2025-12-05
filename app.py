import streamlit as st
from utils.auth_handler import check_auth_and_show_login
from utils.app_common import setup_common
from utils.routes import render_page
from components.common.header import render_header

# 설정은 앱 시작 시 1회만
st.set_page_config(
    page_title="체력 FIT",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 사이드바 숨기기 (로그인 후 메인 페이지에서)
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
[data-testid="collapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# 💥 인증 먼저 검사 (로그인 또는 회원가입 페이지 렌더 후 stop)
check_auth_and_show_login()

# 로그인 성공한 경우에만 공통 세팅 적용
setup_common()

render_header()
render_page()
