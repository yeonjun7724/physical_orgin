"""헤더 컴포넌트"""
import streamlit as st
import os
import inspect
from utils.auth import is_authenticated, get_current_user
from other_pages.login import logout
from utils.routes import PAGE_FILE_MAP


def _get_current_page_name():
    """현재 실행 중인 페이지 이름을 감지"""
    # 현재 실행 중인 파일명 확인 (가장 정확한 방법)
    try:
        frame = inspect.currentframe()
        # AppHeader() -> setup_common() -> 페이지 파일 순서로 프레임이 쌓임
        # 따라서 여러 프레임을 확인해야 함
        frames_to_check = []
        while frame:
            frames_to_check.append(frame)
            frame = frame.f_back
            # 너무 깊이 들어가지 않도록 제한
            if len(frames_to_check) > 20:
                break
        
        # 프레임을 역순으로 확인 (가장 최근 호출된 페이지 파일 찾기)
        for frame in reversed(frames_to_check):
            filename = frame.f_globals.get('__file__', '')
            if filename:
                script_filename = os.path.basename(filename)
                
                # app.py인 경우
                if script_filename == "app.py":
                    return "app"
                
                # PAGE_FILE_MAP의 값과 비교하여 key 찾기
                for page_key, page_filename in PAGE_FILE_MAP.items():
                    if script_filename == page_filename:
                        return page_key
    except:
        pass
    
    # 파일명 기반 감지가 실패한 경우에만 session_state 확인
    current_page = st.session_state.get("page")
    if current_page and current_page in PAGE_FILE_MAP:
        return current_page
    
    # 기본값
    return "home"


def AppHeader():
    """앱 헤더 컴포넌트"""
    # 현재 페이지 이름 가져오기
    current_page_name = _get_current_page_name()
    
    # 페이지 이름을 한글로 변환
    page_display_names = {
        "app": "체력왕 FIT",
        "home": "홈",
        "select_exercise": "운동 선택",
        "ranking": "랭킹",
        "profile": "프로필",
        "store": "상점",
        "setting": "설정",
    }
    display_name = page_display_names.get(current_page_name, current_page_name)
    
    # 헤더 컨테이너
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            f"""
            <h3 style="margin: 0; color: #4c84af; ">💪 {display_name}</h3>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        if is_authenticated():
            user = get_current_user()
            # 사용자명과 로그아웃 버튼을 같은 행에 배치
            name_col, btn_col = st.columns([2, 1])
            with name_col:
                st.markdown(
                    f"""
                    <div style="padding: 0.5rem 0; text-align: right;">
                        <div style="color: #666; font-size: 1rem;">{user['user_name']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with btn_col:
                # 로그아웃 버튼 스타일 - 전역 스타일로 적용
                if not st.session_state.get('_logout_btn_style_added', False):
                    st.markdown(
                        """
                        <style>
                        /* 모든 secondary 버튼에 적용 - 더 강력한 선택자 */
                        button[kind="secondary"],
                        button[data-testid="baseButton-secondary"],
                        div[data-testid="stButton"] > button[kind="secondary"],
                        div[data-testid="stButton"] button,
                        button.st-emotion-cache-1n76uvr {
                            font-size: 0.65rem !important;
                            padding: 0.2rem 0.4rem !important;
                            line-height: 1.1 !important;
                            min-height: auto !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.session_state._logout_btn_style_added = True
                if st.button("logout", key="logout_btn", use_container_width=True):
                    logout()
    
    # 하단 테두리
    st.markdown(
        """
        <div style="border-bottom: 2px solid #4c84af; margin-bottom: 1.5rem;"></div>
        """,
        unsafe_allow_html=True
    )


