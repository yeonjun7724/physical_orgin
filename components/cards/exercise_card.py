"""운동 아이템 카드 컴포넌트 (리뉴얼 버전)"""
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
    """
    UI/디자인 모두 개선한 버전.
    """
    # ---------------------------------------------------------
    # 🌈 CSS — 한 번만 로드
    # ---------------------------------------------------------
    if not st.session_state.get("_exercise_card_style_loaded", False):
        st.markdown("""
        <style>
        /* 카드 기본 레이아웃 */
        .exercise-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e5e5e5;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
            transition: 0.25s ease;
        }
        .exercise-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 8px 24px rgba(76, 132, 175, 0.18);
            border-color: #4c84af;
        }
        /* 상단 영역 (이미지 + 텍스트) */
        .exercise-card-header {
            display: flex;
            gap: 1.25rem;
            align-items: flex-start;
        }
        /* 이미지 통일 */
        .exercise-card-image {
            width: 150px;
            height: 150px;
            border-radius: 14px;
            object-fit: cover;
            box-shadow: 0 3px 12px rgba(0,0,0,0.18);
            flex-shrink: 0;
        }
        /* 제목 */
        .exercise-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #1a1a1a;
            margin: 0;
            line-height: 1.2;
        }
        /* 설명 */
        .exercise-desc {
            margin-top: 0.5rem;
            color: #555;
            font-size: 1rem;
            line-height: 1.55;
        }
        /* 메타정보 영역 */
        .exercise-meta {
            display: flex;
            justify-content: space-between;
            margin: 1.4rem 0 1.2rem 0;
            padding: 0.85rem 0;
            border-top: 1px solid #f0f0f0;
            border-bottom: 1px solid #f0f0f0;
        }
        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.35rem;
            color: #666;
            font-size: 1rem;
        }
        /* 시작하기 버튼 강화 */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #4c84af, #5ba4c7) !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            padding: 0.85rem 1rem !important;
            border: none !important;
            width: 100% !important;
            transition: 0.25s ease !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #3a6a8a, #4c84af) !important;
            transform: translateY(-2px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state["_exercise_card_style_loaded"] = True

    # ---------------------------------------------------------
    # 이미지 Base64 변환
    # ---------------------------------------------------------
    IMG_MAP = {
        "pushup": "assets/image/exercise/pushup.png",
        "situp": "assets/image/exercise/situp.png",
        "squat": "assets/image/exercise/squat.png",
        "balance": "assets/image/exercise/balance.png",
        "knee_lift": "assets/image/exercise/jump.png",
        "trunk_flex": "assets/image/exercise/run.png",
    }

    def load_image(path: str):
        try:
            base = Path(__file__).resolve().parent.parent.parent
            full = base / path
            if not full.exists():
                return None
            data = full.read_bytes()
            encoded = base64.b64encode(data).decode()
            ext = full.suffix.replace(".", "")
            return f"data:image/{ext};base64,{encoded}"
        except:
            return None

    img_path = IMG_MAP.get(key)
    img_b64 = load_image(img_path) if img_path else None

    # ---------------------------------------------------------
    # HTML Body
    # ---------------------------------------------------------
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)

    # Header Section
    if img_b64:
        st.markdown(
            f"""<div class="exercise-card-header">
                <img src="{img_b64}" class="exercise-card-image" />
                <div class="exercise-card-text">
                    <div class="exercise-title">{name}</div>
                    <div class="exercise-desc">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div class="exercise-card-header">
                <div style="font-size:4rem;">{icon}</div>
                <div>
                    <div class="exercise-title">{name}</div>
                    <div class="exercise-desc">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 메타 정보
    st.markdown(
        f"""<div class="exercise-meta">
            <div class="meta-item">⏱️ {duration_label}</div>
            <div class="meta-item">📊 난이도: {difficulty_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 버튼
    if st.button("시작하기", key=f"start_{key}", type="primary"):
        if on_start:
            on_start()

    st.markdown("</div>", unsafe_allow_html=True)
