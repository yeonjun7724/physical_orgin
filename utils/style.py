# utils/style.py
import streamlit as st
import os

# 현재 파일의 디렉토리 기준으로 경로 설정
_current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
   theme_path = os.path.join(_current_dir, "assets", "theme.css")
   with open(theme_path, "r", encoding="utf-8") as _f:
      THEME_CSS = _f.read()
except Exception:
   THEME_CSS = ""

def get_theme_css() -> str:
   return THEME_CSS

def apply_global_css():
   try:
      components_path = os.path.join(_current_dir, "components", "components.css")
      with open(components_path, "r", encoding="utf-8") as _fc:
         COMPONENTS_CSS = _fc.read()
   except Exception:
      COMPONENTS_CSS = ""

   st.markdown(
      """
      <style>
      """ + THEME_CSS + "\n" + COMPONENTS_CSS + "\n" + """
      body { font-family: 'Pretendard', sans-serif; }
      .stButton button { transition: 0.2s all ease-in-out; }
      .stButton button:hover { transform: scale(1.02); }
      </style>
      """,
      unsafe_allow_html=True,
   )
