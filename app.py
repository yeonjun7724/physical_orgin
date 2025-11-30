import streamlit as st
from utils.app_common import setup_common
from utils.routes import render_page
from components.common.header import render_header

st.set_page_config(page_title="체력왕 FIT", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
[data-testid="collapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

setup_common()

# 상단 헤더 렌더링
render_header()

# 페이지 렌더링
render_page()
