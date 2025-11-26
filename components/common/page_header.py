"""페이지 헤더 컴포넌트"""
import streamlit as st


def PageHeader(title: str, description: str, icon: str = ""):
    """
    페이지 헤더 컴포넌트
    
    여러 페이지에서 공통으로 사용되는 페이지 헤더입니다.
    
    사용 위치:
    - app.py: 메인 페이지 헤더
    - pages/02_select_exercise.py: 운동 선택 페이지
    - pages/03_ranking.py: 랭킹 페이지
    - pages/04_profile.py: 프로필 페이지
    - pages/05_store.py: 상점 페이지
    - pages/06_setting.py: 설정 페이지
    - other_pages/info_update.py: 내정보 수정 페이지
    - other_pages/account_settings.py: 계정 설정 페이지
    - other_pages/confirm_to_info_update.py: 비밀번호 확인 페이지
    
    사용 예시:
        PageHeader("홈", "홈 페이지입니다", "🏠")
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin: 0; color: #4c84af; font-size: 1.75rem; font-weight: 700;">{icon} {title}</h1>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

