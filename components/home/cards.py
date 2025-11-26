"""홈 페이지 카드 컴포넌트"""
import streamlit as st


def GreetingCard(user_name: str):
    """
    인사말 카드 컴포넌트
    
    사용 위치:
    - pages/01_home.py: 홈 페이지 상단 인사말
    
    사용 예시:
        GreetingCard("체력왕")
    """
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #4c84af, #81bfc7); padding: 2rem; border-radius: 12px; 
                    color: white; margin-bottom: 2rem; text-align: center;">
            <h2 style="margin: 0; color: white;">안녕하세요, {user_name}님! 👋</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">오늘도 체력 측정을 시작해볼까요?</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def ActionButtonGrid(buttons: list):
    """
    액션 버튼 그리드 컴포넌트
    
    사용 위치:
    - pages/01_home.py: 홈 페이지의 메인 액션 버튼들
    
    사용 예시:
        ActionButtonGrid([
            {"label": "💪 바로 측정하기", "key": "quick_measure", "type": "primary", 
             "on_click": lambda: go_to("select_exercise")}
        ])
    """
    cols = st.columns(len(buttons))
    for i, button_config in enumerate(buttons):
        with cols[i]:
            if st.button(
                button_config.get("label", ""),
                key=button_config.get("key", f"btn_{i}"),
                use_container_width=True,
                type=button_config.get("type", "secondary"),
                help=button_config.get("help", "")
            ):
                if "on_click" in button_config:
                    button_config["on_click"]()


def ResultSummaryCard(score: str, grade: str, percentile: str, metrics: dict):
    """
    결과 요약 카드 컴포넌트
    
    사용 위치:
    - pages/01_home.py: 홈 페이지의 최근 측정 결과 섹션
    
    사용 예시:
        ResultSummaryCard(
            score="67점", grade="3등급", percentile="28",
            metrics={"횟수": "35회", "정확도": "92%", "템포": "1.2s"}
        )
    """
    metrics_html = "".join([f'<div><strong>{k}:</strong> {v}</div>' for k, v in metrics.items()])
    st.markdown(
        f"""
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0; color: #1976d2;">📊 최근 측정 결과</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                <div><strong>점수:</strong> {score}</div>
                <div><strong>등급:</strong> {grade}</div>
                <div><strong>상위:</strong> {percentile}%</div>
                {metrics_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def FeedItem(name: str, exercise: str, score: str, time: str, likes: int = 0):
    """
    피드 아이템 컴포넌트
    
    사용 위치:
    - pages/01_home.py: 홈 페이지의 최근 활동 피드 섹션
    
    사용 예시:
        FeedItem("김철수", "팔굽혀펴기", "85점", "2시간 전", 12)
    """
    st.markdown(
        f"""
        <div style="padding: 1rem; background: white; border: 1px solid #eee; border-radius: 8px; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{name}</strong>님이 <strong>{exercise}</strong>에서 <strong>{score}</strong>을 기록했습니다
                    <div style="color: #999; font-size: 0.9rem; margin-top: 0.25rem;">{time}</div>
                </div>
                <div style="color: #4c84af;">❤️ {likes}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

