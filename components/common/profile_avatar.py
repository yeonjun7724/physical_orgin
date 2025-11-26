"""프로필 아바타 컴포넌트"""
import streamlit as st
import os
import base64


def ProfileAvatar(name: str, age: str, gender: str, icon: str = "👤", level: int = 100, image_path: str = None, show_info: bool = True):
    """
    프로필 아바타 컴포넌트
    
    여러 페이지에서 공통으로 사용되는 프로필 아바타입니다.
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 프로필 정보
    - pages/06_setting.py: 설정 페이지의 프로필 설정
    - other_pages/info_update.py: 내정보 수정 페이지
    
    사용 예시:
        ProfileAvatar("체력왕김민수", "20대", "남성", image_path="assets/image/character.png")
        ProfileAvatar("체력왕김민수", "20대", "남성", "👤", 100)  # 이모지 사용
        ProfileAvatar("체력왕김민수", "20대", "남성", show_info=False)  # 사진만 표시
    """
    # 이미지 경로가 없으면 기본값 사용
    if image_path is None:
        image_path = "assets/image/character.png"
    
    # 이미지 HTML 생성
    avatar_html = ""
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
                    avatar_html = f'<img src="data:image/{img_ext};base64,{img_data}" alt="{name}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin-bottom: 0.5rem; border: 3px solid #4c84af; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
            except Exception:
                # 이미지 로드 실패 시 아이콘으로 대체
                avatar_html = f'<div style="font-size: 4rem; margin-bottom: 0.5rem;">{icon}</div>'
        else:
            # 파일이 없으면 아이콘으로 대체
            avatar_html = f'<div style="font-size: 4rem; margin-bottom: 0.5rem;">{icon}</div>'
    else:
        # 이미지 경로가 없으면 아이콘 사용
        avatar_html = f'<div style="font-size: 4rem; margin-bottom: 0.5rem;">{icon}</div>'
    
    # 정보 표시 여부에 따라 HTML 생성
    if show_info:
        info_html = f'<div style="font-weight: 600; font-size: 1.2rem; margin-bottom: 0.25rem;">{name}</div><div style="color: #666; margin-bottom: 0.25rem;">{age} · {gender}</div><div style="color: #4c84af; font-weight: 600;">Lv. {level}</div>'
    else:
        info_html = ""
    
    # 전체 HTML 조합
    full_html = f'<div style="text-align: center; padding: 1rem;">{avatar_html}{info_html}</div>'
    
    st.markdown(full_html, unsafe_allow_html=True)

