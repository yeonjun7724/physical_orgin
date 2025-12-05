"""홈 페이지 카드 컴포넌트"""
import streamlit as st


def GreetingCard(user_name: str, scroll_target_id: str = None):
    """
    인사말 카드 컴포넌트
    
    사용 위치:
    - pages/02_home.py: 홈 페이지 상단 인사말
    
    사용 예시:
        GreetingCard("체력", scroll_target_id="exercise-selection")
    """
    card_id = "greeting-card"
    cursor_style = "cursor: pointer;"
    script = ""
    
    if scroll_target_id:
        script = f"""
        <script>
        (function() {{
            const card = document.getElementById('{card_id}');
            if (card && !card.dataset.listenerAdded) {{
                card.dataset.listenerAdded = 'true';
                card.addEventListener('click', function() {{
                    const target = document.getElementById('{scroll_target_id}');
                    if (target) {{
                        target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }}
                }});
            }}
        }})();
        </script>
        """
    
    st.markdown(
        f"""
        <div id="{card_id}" style="background: linear-gradient(135deg, #4c84af, #81bfc7); padding: 2rem; border-radius: 12px; 
                    color: white; margin-bottom: 2rem; text-align: center; {cursor_style} transition: transform 0.2s ease;">
            <h2 style="margin: 0; color: white;">안녕하세요, {user_name}님! 👋</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">오늘도 체력 측정을 시작해볼까요?</p>
        </div>
        {script}
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
            "on_click": lambda: go_to("home")}
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


def ResultSummaryCard(score: str, grade: str, percentile: str, metrics: dict, exercise_name: str = ""):
    """
    결과 요약 카드 컴포넌트
    
    사용 위치:
    - pages/02_home.py: 홈 페이지의 최근 측정 결과 섹션
    
    사용 예시:
        ResultSummaryCard(
            score="67점", grade="3등급", percentile="28",
            metrics={"횟수": "35회", "정확도": "92%", "템포": "1.2s"},
            exercise_name="팔굽혀펴기"
        )
    """
    metrics_html = "".join([f'<div style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong style="font-size: 1.2rem;">{k}:</strong> <span style="font-size: 1.2rem;">{v}</span></div>' for k, v in metrics.items()])
    exercise_html = f'<div style="font-size: 1.3rem; font-weight: bold; color: #1976d2; margin-bottom: 1rem;">{exercise_name}</div>' if exercise_name else ""
    st.markdown(
        f"""<div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; height: 100%;">
            <h3 style="margin: 0 0 1rem 0; color: #1976d2; font-size: 1.4rem;">📊 최근 측정 결과</h3>
            {exercise_html}<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                <div style="font-size: 1.1rem;"><strong style="font-size: 1.2rem;">점수:</strong> <span style="font-size: 1.2rem;">{score}</span></div>
                <div style="font-size: 1.1rem;"><strong style="font-size: 1.2rem;">등급:</strong> <span style="font-size: 1.2rem;">{grade}</span></div>
                <div style="font-size: 1.1rem;"><strong style="font-size: 1.2rem;">상위:</strong> <span style="font-size: 1.2rem;">{percentile}%</span></div>
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

