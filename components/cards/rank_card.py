"""랭킹 페이지 카드 컴포넌트"""
import streamlit as st


def MyRankCard(rank: int, percentile: str, total_score: int, grade: str, reward: str = ""):
    """
    내 순위 카드 (리뉴얼 버전)
    좌측: 내 순위 크게
    우측: 상위 %, 총점, 등급 묶어서 세로 정렬
    아래: 주간 보상 (폰트 크게)
    
    Args:
        rank: 순위 (999는 랭킹 미등록을 의미)
    """
    """
    내 순위 카드 (리뉴얼 버전)
    좌측: 내 순위 크게
    우측: 상위 %, 총점, 등급 묶어서 세로 정렬
    아래: 주간 보상 (폰트 크게)
    """

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #4c84af, #81bfc7);
            padding: 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
        ">
            <!-- 상단 좌/우 구조 -->
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
            <!-- 왼쪽: 내 순위 -->
            <div>
                <div style="font-size: 1.2rem; opacity: 0.9;">내 순위</div>
                <div style="font-size: 4.5rem; font-weight: 800; line-height: 1;">
                    {rank if rank < 999 else "-"}위
                </div>
            </div>
            <!-- 오른쪽: 상위/총점/등급 -->
            <div style="display: flex; flex-direction: column; gap: 1rem; text-align: right;">
                <div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">상위</div>
                    <div style="font-size: 2.2rem; font-weight: bold;">{percentile}%</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">총점</div>
                    <div style="font-size: 2.2rem; font-weight: bold;">{total_score}점</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">등급</div>
                    <div style="font-size: 2.2rem; font-weight: bold;">{grade}</div>
                </div>
            </div>
        </div>
        <!-- 주간 보상 -->
        {f'''<div style="
            margin-top: 1.8rem;
            padding-top: 1.2rem;
            border-top: 1px solid rgba(255,255,255,0.4);
            font-size: 1.3rem;
            font-weight: 600;
        ">{reward}</div>
        ''' if reward else ""}
        
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
        <div style="background: {'#fff9e6' if rank <= 3 else '#f9f9f9'}; padding: 1rem; border-radius: 8px; 
                    border: {'2px solid #ffd700' if rank <= 3 else '1px solid #eee'}; 
                    display: flex; align-items: center; gap: 1rem; height: auto;">
            <div style="font-size: 2.5rem; flex-shrink: 0;">{medal_emoji}</div>
            <div style="flex: 1;">
                <div style="font-size: 1.2rem; font-weight: bold; color: #4c84af; margin-bottom: 0.25rem;">{rank}위</div>
                <div style="font-weight: 600; margin-bottom: 0.25rem; font-size: 1rem;">{name}</div>
                <div style="color: #666; font-size: 0.9rem;">{score}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

