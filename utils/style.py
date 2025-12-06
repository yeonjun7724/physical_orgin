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

   # Exercise Card CSS
   EXERCISE_CARD_CSS = """
      .exercise-card {
         background: #ffffff;
         border-radius: 16px;
         padding: 1.2rem;
         margin: 1.2rem 0;
         border: 1px solid #e6e6e6;
         box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
      }
      .exercise-card-header {
         display: flex;
         gap: 1.2rem;
         align-items: center;
      }
      .exercise-card-image {
         width: 140px;
         height: 105px;
         border-radius: 12px;
         object-fit: cover;
         background: #f4f4f4;
         box-shadow: 0 3px 10px rgba(0,0,0,0.15);
      }
      .exercise-title {
         font-size: 1.8rem;
         font-weight: 800;
         color: #222;
         margin: 0;
         line-height: 1;
      }
      .exercise-desc {
         margin-top: 0.4rem;
         color: #555;
         font-size: 0.95rem;
         line-height: 1.4;
      }
      .exercise-meta {
         display: flex;
         justify-content: space-between;
         margin: 1rem 0 1rem 0;
         padding: 0.7rem 0;
         border-top: 1px solid #eee;
         border-bottom: 1px solid #eee;
         font-size: 0.95rem;
         color: #666;
      }
      /* 카드 내부 버튼 컨테이너 전체 너비 */
      .exercise-card div[data-testid="stButton"],
      .exercise-card-button-container div[data-testid="stButton"] {
         width: 100% !important;
         max-width: 100% !important;
      }
      /* 버튼 전체 너비 및 스타일 */
      .exercise-card div[data-testid="stButton"] > button,
      .exercise-card-button-container div[data-testid="stButton"] > button,
      div[data-testid="stButton"] > button[kind="primary"] {
         width: 100% !important;
         max-width: 100% !important;
         background: linear-gradient(135deg, #4c84af, #5ba4c7) !important;
         color: white !important;
         border-radius: 10px !important;
         font-size: 1rem !important;
         font-weight: 700 !important;
         padding: 0.7rem 1rem !important;
         border: none !important;
      }
   """

   st.markdown(
      """
      <style>
      """ + THEME_CSS + "\n" + COMPONENTS_CSS + "\n" + EXERCISE_CARD_CSS + """
      body { font-family: 'Pretendard', sans-serif; }
      .stButton button { transition: 0.2s all ease-in-out; }
      .stButton button:hover { transform: scale(1.02); }
      </style>
      """,
      unsafe_allow_html=True,
   )
   st.markdown("""
   <style>
   div[data-testid="stVerticalBlock"] > div:empty {
      display: none !important;
   }
   </style>
   """, unsafe_allow_html=True)

