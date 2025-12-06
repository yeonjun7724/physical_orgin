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

    # 첫 번째 행: 이미지와 정보를 2열로 배치
    col1, col2 = st.columns([1.1, 2.5], gap="medium")

    # ---------------- 왼쪽 열: 이미지 ----------------
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

    # ---------------- 오른쪽 열: 운동 이름, 설명, 시간/난이도 ----------------
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

    # 두 번째 행: 시작하기 버튼 (전체 너비)
    # 버튼을 카드 div 안에 확실히 포함시키기 위해 컨테이너 사용
    st.markdown('<div class="exercise-card-button-container">', unsafe_allow_html=True)
    if st.button("시작하기", key=f"start_{key}", type="primary", use_container_width=True):
        if on_start:
            on_start()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
