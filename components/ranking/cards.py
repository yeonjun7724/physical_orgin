"""랭킹 페이지 카드 컴포넌트"""
import streamlit as st


def MyRankCard(rank: int, percentile: str, total_score: int, grade: str, reward: str = ""):
    """
    내 순위 카드 컴포넌트
    
    사용 위치:
    - pages/03_ranking.py: 랭킹 페이지의 내 순위 표시
    
    사용 예시:
        MyRankCard(rank=47, percentile="12", total_score=85, grade="2등급", reward="주간 보상: +200 FIT")
    """
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #4c84af, #81bfc7); padding: 2rem; border-radius: 12px; 
                    color: white; margin-bottom: 2rem; text-align: center;">
            <h2 style="margin: 0; color: white;">내 순위</h2>
            <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">{rank}위</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                <div><div style="font-size: 0.9rem; opacity: 0.9;">상위</div><div style="font-size: 1.2rem; font-weight: bold;">{percentile}%</div></div>
                <div><div style="font-size: 0.9rem; opacity: 0.9;">총점</div><div style="font-size: 1.2rem; font-weight: bold;">{total_score}점</div></div>
                <div><div style="font-size: 0.9rem; opacity: 0.9;">등급</div><div style="font-size: 1.2rem; font-weight: bold;">{grade}</div></div>
            </div>
            {f'<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);">{reward}</div>' if reward else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def RankCard(rank: int, name: str, score: str):
    """
    랭킹 카드 컴포넌트 (상위 3명용)
    
    사용 위치:
    - pages/03_ranking.py: 랭킹 페이지의 상위 3명 표시
    
    사용 예시:
        RankCard(rank=1, name="체력왕김철수", score="98점")
    """
    medal_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else ""
    st.markdown(
        f"""
        <div style="background: {'#fff9e6' if rank <= 3 else '#f9f9f9'}; padding: 1.5rem; border-radius: 8px; 
                    border: {'2px solid #ffd700' if rank <= 3 else '1px solid #eee'}; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{medal_emoji}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #4c84af;">{rank}위</div>
            <div style="margin: 0.5rem 0; font-weight: 600;">{name}</div>
            <div style="color: #666;">{score}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

