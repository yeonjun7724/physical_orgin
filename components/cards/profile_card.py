"""프로필 페이지 카드 컴포넌트"""
import streamlit as st


def StatCard(value: str, label: str, color: str = "#4c84af"):
    """
    통계 카드 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 통계 정보 표시
    
    사용 예시:
        StatCard("85점", "종합 점수", COLORS["MAIN_BLUE"])
    """
    st.markdown(
        f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.25rem;">{value}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def BadgeCard(name: str, icon: str, desc: str, earned: bool = False):
    """
    뱃지 카드 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 뱃지 섹션
    
    사용 예시:
        BadgeCard("연속 측정왕", "🔥", "7일 연속 측정", earned=True)
    """
    opacity = "1" if earned else "0.3"
    st.markdown(
        f"""
        <div style="background: {'#e3f2fd' if earned else '#f5f5f5'}; padding: 1.5rem; border-radius: 8px; 
                    text-align: center; border: {'2px solid #4c84af' if earned else '1px solid #ddd'}; opacity: {opacity};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">{name}</div>
            <div style="font-size: 0.85rem; color: #666;">{desc}</div>
            {f'<div style="margin-top: 0.5rem; color: #4c84af; font-size: 0.8rem;">✓ 획득</div>' if earned else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def GradeProgressBar(current_grade: str, next_grade: str, progress: int):
    """
    등급 진행률 바 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 등급 정보 섹션
    
    사용 예시:
        GradeProgressBar(current_grade="2등급", next_grade="1등급", progress=75)
    """
    st.markdown(
        f"""
        <div style="padding: 1.5rem; background: #f9f9f9; border-radius: 8px; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">현재: {current_grade}</span>
                <span style="font-weight: 600;">다음: {next_grade}</span>
            </div>
            <div style="background: #e0e0e0; border-radius: 4px; height: 30px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #4c84af, #81bfc7); height: 100%; width: {progress}%; 
                            display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;">
                    {progress}%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def GradeCard(grade: str, min_score: int, desc: str, color: str, is_current: bool = False):
    """
    등급 카드 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 등급 정보 섹션
    
    사용 예시:
        GradeCard(grade="2등급", min_score=80, desc="우수 등급", 
                 color=COLORS["MAIN_BLUE"], is_current=True)
    """
    border = f"3px solid {color}" if is_current else "1px solid #ddd"
    st.markdown(
        f"""
        <div style="background: {'#e3f2fd' if is_current else '#f9f9f9'}; padding: 1rem; border-radius: 8px; 
                    border: {border}; text-align: center;">
            <div style="font-weight: 600; font-size: 1.1rem; color: {color}; margin-bottom: 0.25rem;">{grade}</div>
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.25rem;">{min_score}점 이상</div>
            <div style="font-size: 0.85rem; color: #999;">{desc}</div>
            {f'<div style="margin-top: 0.5rem; color: {color}; font-weight: 600;">현재 등급</div>' if is_current else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def PointsCard(points: int, label: str, button_text: str = "", button_onclick: str = ""):
    """
    포인트 카드 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 FIT 포인트 표시
    - pages/06_setting.py: 설정 페이지의 FIT 포인트 표시
    
    사용 예시:
        PointsCard(1250, "FIT 포인트", "상점 가기", "window.location.href='?page=store'")
        PointsCard(1250, "FIT 포인트")  # 버튼 없이 표시
    """
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #ffd700, #ffed4e); padding: 1.5rem; border-radius: 12px; 
                    text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; color: #666;">{label}</div>
            <div style="font-size: 2rem; font-weight: bold; color: #222; margin-bottom: 1rem;">{points:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if button_text:
        if st.button(button_text, use_container_width=True, key="points_card_button"):
            if button_onclick:
                st.markdown(f"<script>{button_onclick}</script>", unsafe_allow_html=True)


def ActionButtonsRow(buttons: list):
    """
    액션 버튼 행 컴포넌트
    
    사용 위치:
    - pages/04_profile.py: 프로필 페이지의 설정/공유 버튼
    
    사용 예시:
        ActionButtonsRow([
            {"label": "⚙️ 설정", "key": "settings", "on_click": lambda: st.info("설정")}
        ])
    """
    cols = st.columns(len(buttons))
    for i, button_config in enumerate(buttons):
        with cols[i]:
            if st.button(
                button_config.get("label", ""),
                key=button_config.get("key", f"action_btn_{i}"),
                use_container_width=True
            ):
                if "on_click" in button_config:
                    button_config["on_click"]()

