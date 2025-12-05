import streamlit as st
import base64
from pathlib import Path


def ExerciseItemCard(
    name: str,
    description: str,
    duration_label: str,
    difficulty_label: str,
    icon: str,
    key: str,
    on_start=None
):

    # ---------------------------------------------------------
    # CSS 한 번만 로딩
    # ---------------------------------------------------------
    if not st.session_state.get("_exercise_card_style_loaded_v2", False):
        st.markdown("""
        <style>
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
        /* 이미지 비율 강제: 4:3 */
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
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #4c84af, #5ba4c7) !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            padding: 0.7rem 1rem !important;
            border: none !important;
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state["_exercise_card_style_loaded_v2"] = True

    # ---------------------------------------------------------
    # 이미지 불러오기
    # ---------------------------------------------------------
    IMG_MAP = {
        "pushup": "assets/image/exercise/pushup.png",
        "situp": "assets/image/exercise/situp.png",
        "squat": "assets/image/exercise/squat.png",
        "balance": "assets/image/exercise/balance.png",
        "knee_lift": "assets/image/exercise/knee_lift.jpg",
        "trunk_flex": "assets/image/exercise/trunk_flex.jpg",
    }

    def load_image(path: str):
        try:
            base = Path(__file__).resolve().parent.parent.parent
            full = base / path
            if not full.exists():
                return None
            encoded = base64.b64encode(full.read_bytes()).decode()
            ext = full.suffix.replace(".", "")
            return f"data:image/{ext};base64,{encoded}"
        except:
            return None

    img_path = IMG_MAP.get(key)
    img_b64 = load_image(img_path)

    # ---------------------------------------------------------
    # 카드 UI
    # ---------------------------------------------------------
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 2.5], gap="medium")

    # ---------------- 왼쪽 이미지 ----------------
    with col1:
        if img_b64:
            st.markdown(
                f'<img src="{img_b64}" class="exercise-card-image" />',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="font-size:3rem; text-align:center; padding:1rem;">{icon}</div>',
                unsafe_allow_html=True
            )

    # ---------------- 오른쪽 텍스트 ----------------
    with col2:
        st.markdown(f'<div class="exercise-title">{name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exercise-desc">{description}</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="exercise-meta">
                <div>⏱️ {duration_label}</div>
                <div>📊 난이도: {difficulty_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("시작하기", key=f"start_{key}", type="primary", use_container_width=True):
            if on_start:
                on_start()

    st.markdown("</div>", unsafe_allow_html=True)
