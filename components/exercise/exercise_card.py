"""운동 아이템 컴포넌트"""
import streamlit as st
import os
import base64
from pathlib import Path


def _get_exercise_image_path(key: str) -> str | None:
    """운동 종목 key에 해당하는 이미지 경로 반환"""
    image_map = {
        "pushup": "assets/image/exercise/pushup.png",
        "situp": "assets/image/exercise/situp.png",
        "squat": "assets/image/exercise/squat.png",
        "balance": "assets/image/exercise/balance.png",
        "knee_lift": "assets/image/exercise/jump.png",
        "trunk_flex": "assets/image/exercise/run.png",
    }
    return image_map.get(key)


def _get_image_base64(image_path: str) -> str | None:
    """이미지 파일을 base64로 인코딩"""
    try:
        current_dir = Path(__file__).parent.parent.parent
        full_path = current_dir / image_path
        
        if full_path.exists():
            with open(full_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                img_ext = full_path.suffix[1:]  # .png -> png
                return f"data:image/{img_ext};base64,{img_data}"
    except Exception:
        pass
    return None


def ExerciseItemCard(name: str, description: str, duration_label: str, difficulty_label: str, 
                    icon: str, key: str, on_start):
    """
    운동 종목 카드 컴포넌트
    
    사용 위치:
    - pages/02_select_exercise.py: 운동 종목 선택 페이지
    
    사용 예시:
        ExerciseItemCard(
            name="팔굽혀펴기",
            description="상체 근지구력을 측정합니다",
            duration_label="약 1분",
            difficulty_label="2/3",
            icon="💪",
            key="pushup",
            on_start=lambda: go_to("tutorial")
        )
    """
    # 스타일 추가 (한 번만)
    if not st.session_state.get('_exercise_card_styles_added', False):
        st.markdown(
            """
            <style>
            .exercise-card-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border: 1px solid #e0e0e0;
                border-radius: 16px;
                padding: 1.25rem;
                margin-bottom: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            .exercise-card-container:hover {
                box-shadow: 0 6px 16px rgba(76, 132, 175, 0.15);
                transform: translateY(-2px);
                border-color: #4c84af;
            }
            .exercise-card-image {
                width: 120px;
                height: 120px;
                object-fit: cover;
                border-radius: 12px;
                flex-shrink: 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            .exercise-card-header {
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                margin-bottom: 0.75rem;
            }
            .exercise-card-icon {
                font-size: 2.5rem;
                line-height: 1;
                flex-shrink: 0;
            }
            .exercise-card-content {
                flex: 1;
            }
            .exercise-card-title {
                font-size: 1.4rem;
                font-weight: 700;
                color: #222;
                margin: 0;
                line-height: 1.3;
            }
            .exercise-card-desc {
                font-size: 0.9rem;
                color: #666;
                margin: 0.5rem 0 0 0;
                line-height: 1.5;
                font-weight: 400;
            }
            .exercise-card-meta {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin: 0.75rem 0;
                padding: 0.5rem 0;
                border-top: 1px solid #f0f0f0;
                border-bottom: 1px solid #f0f0f0;
            }
            .exercise-card-meta-item {
                display: flex;
                align-items: center;
                gap: 0.35rem;
                font-size: 0.8rem;
                color: #666;
            }
            .exercise-card-button-wrapper {
                margin-top: auto;
                padding-top: 0.75rem;
            }
            /* 연한 색상의 시작하기 버튼 스타일 */
            div[data-testid="stButton"] > button[kind="primary"] {
                background-color: rgba(76, 132, 175, 0.12) !important;
                color: #4c84af !important;
                border: 1.5px solid rgba(76, 132, 175, 0.25) !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
            }
            div[data-testid="stButton"] > button[kind="primary"]:hover {
                background-color: rgba(76, 132, 175, 0.2) !important;
                border-color: rgba(76, 132, 175, 0.4) !important;
                transform: scale(1.02);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.session_state._exercise_card_styles_added = True
    
    # 카드 컨테이너
    st.markdown('<div class="exercise-card-container">', unsafe_allow_html=True)
    
    # 이미지 가져오기
    image_path = _get_exercise_image_path(key)
    image_html = ""
    if image_path:
        image_base64 = _get_image_base64(image_path)
        if image_base64:
            image_html = f'<img src="{image_base64}" alt="{name}" class="exercise-card-image">'
    
    # 헤더 (이미지 + 제목/설명)
    if image_html:
        st.markdown(
            f"""
            <div class="exercise-card-header">
                {image_html}
                <div class="exercise-card-content">
                    <div class="exercise-card-title">{name}</div>
                    <div class="exercise-card-desc">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # 이미지가 없으면 아이콘 사용
        st.markdown(
            f"""
            <div class="exercise-card-header">
                <div class="exercise-card-icon">{icon}</div>
                <div class="exercise-card-content">
                    <div class="exercise-card-title">{name}</div>
                    <div class="exercise-card-desc">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # 메타 정보
    st.markdown(
        f"""
        <div class="exercise-card-meta">
            <div class="exercise-card-meta-item">
                <span>⏱️</span>
                <span>{duration_label}</span>
            </div>
            <div class="exercise-card-meta-item">
                <span>📊</span>
                <span>난이도: {difficulty_label}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 버튼 래퍼
    st.markdown('<div class="exercise-card-button-wrapper">', unsafe_allow_html=True)
    if st.button("시작하기", key=f"start_{key}", use_container_width=True, type="primary"):
        on_start()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

