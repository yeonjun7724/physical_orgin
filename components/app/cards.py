"""app.py 전용 카드 컴포넌트"""
import streamlit as st
import os
import base64


def FeatureCard(icon: str, title: str, description: str):
    """
    주요 기능 카드 컴포넌트 (1열, 얇은 카드, 왼쪽에 큰 이모지)
    
    사용 위치:
    - app.py: 서비스 소개 페이지의 주요 기능 섹션
    
    사용 예시:
        FeatureCard("💪", "체력 측정", "6가지 종목으로 나의 체력을 정확하게 측정합니다")
    """
    st.markdown(
        f"""
        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.25rem; 
                    margin-bottom: 1.25rem; display: flex; align-items: center; gap: 1rem; 
                    transition: box-shadow 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="font-size: 2rem; flex-shrink: 0; line-height: 1;">{icon}</div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 0.25rem 0; color: #222; font-size: 1.1rem; font-weight: 600;">{title}</h3>
                <p style="margin: 0; color: #666; font-size: 0.95rem; line-height: 1.5;">{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def ExerciseCarouselCard(name: str, description: str, image_path: str = None, icon: str = "💪", is_last_row: bool = False):
    """
    운동 종목 캐러셀 카드 컴포넌트 (개별 카드)
    
    ExerciseCarouselCard: 개별 카드를 렌더링하는 함수 (이미지, 제목, 설명 포함)
    ExerciseCarousel: 여러 카드를 2열 그리드로 배치하는 함수 (내부에서 ExerciseCarouselCard를 호출)
    
    사용 위치:
    - app.py: ExerciseCarousel 내부에서 사용 (직접 호출하지 않음)
    
    사용 예시:
        ExerciseCarouselCard(
            name="팔굽혀펴기", 
            description="상체 근지구력 측정",
            image_path="assets/image/exercise/pushup.png",
            icon="💪"
        )
    """
    image_html = ""
    if image_path:
        # 이미지 파일 경로를 절대 경로로 변환
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_image_path = os.path.join(current_dir, image_path)
        
        # 이미지 파일이 존재하면 base64로 인코딩
        if os.path.exists(full_image_path):
            try:
                with open(full_image_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                    img_ext = os.path.splitext(full_image_path)[1][1:]  # 확장자 추출 (.png -> png)
                    image_html = f'<img src="data:image/{img_ext};base64,{img_data}" alt="{name}" style="width: 100%; height: 180px; object-fit: cover; border-radius: 8px 8px 0 0; margin-bottom: 0.75rem;">'
            except Exception:
                # 이미지 로드 실패 시 아이콘으로 대체
                image_html = f'<div style="width: 100%; height: 180px; background: linear-gradient(135deg, #4c84af, #81bfc7); border-radius: 8px 8px 0 0; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: center; font-size: 4rem;">{icon}</div>'
        else:
            # 파일이 없으면 아이콘으로 대체
            image_html = f'<div style="width: 100%; height: 180px; background: linear-gradient(135deg, #4c84af, #81bfc7); border-radius: 8px 8px 0 0; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: center; font-size: 4rem;">{icon}</div>'
    else:
        # 이미지가 없으면 아이콘으로 대체
        image_html = f'<div style="width: 100%; height: 180px; background: linear-gradient(135deg, #4c84af, #81bfc7); border-radius: 8px 8px 0 0; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: center; font-size: 4rem;">{icon}</div>'
    
    # 마지막 행이 아닐 때만 하단 여백 추가
    margin_bottom = "0.75rem" if not is_last_row else "0"
    
    st.markdown(
        f"""
        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0; 
                    width: 100%; margin-bottom: {margin_bottom}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;">
            {image_html}
            <div style="padding: 0 1rem 1rem 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #222; font-size: 1rem; font-weight: 600;">{name}</h4>
                <p style="margin: 0; color: #666; font-size: 0.85rem; line-height: 1.4;">{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def ExerciseCarousel(exercises: list):
    """
    운동 종목 그리드 컴포넌트 (2열 3행)
    
    ExerciseCarouselCard: 개별 카드를 렌더링하는 함수
    ExerciseCarousel: 여러 카드를 2열 그리드로 배치하는 함수 (내부에서 ExerciseCarouselCard를 호출)
    
    사용 위치:
    - app.py: 서비스 소개 페이지의 측정 종목 섹션
    
    사용 예시:
        exercises = [
            {"name": "팔굽혀펴기", "description": "상체 근지구력 측정", 
                "icon": "💪", "image_path": "assets/image/exercise/pushup.png"}
        ]
        ExerciseCarousel(exercises)
    """
    # 2열로 나누기
    total_rows = (len(exercises) + 1) // 2  # 전체 행 수 계산
    for row_idx in range(0, len(exercises), 2):
        is_last_row = (row_idx // 2) == (total_rows - 1)  # 마지막 행인지 확인
        cols = st.columns(2, gap="large")
        for j, col in enumerate(cols):
            if row_idx + j < len(exercises):
                exercise = exercises[row_idx + j]
                with col:
                    ExerciseCarouselCard(
                        name=exercise.get("name", ""),
                        description=exercise.get("description", ""),
                        image_path=exercise.get("image_path") or exercise.get("image_url"),  # image_path 또는 image_url 지원
                        icon=exercise.get("icon", "💪"),
                        is_last_row=is_last_row
                    )

