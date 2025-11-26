"""진행률 컴포넌트"""
import streamlit as st


def ProgressBar(label: str, current: int, total: int, reward_label: str = ""):
    """진행률 바 컴포넌트"""
    progress = current / total if total > 0 else 0
    progress_percent = int(progress * 100)
    
    st.markdown(
        f"""
        <div style="padding: 1rem; background: #f9f9f9; border-radius: 8px; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{label}</span>
                <span style="color: #4c84af; font-weight: 600;">{reward_label}</span>
            </div>
            <div style="background: #e0e0e0; border-radius: 4px; height: 24px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #4c84af, #81bfc7); height: 100%; width: {progress_percent}%; 
                            display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; 
                            transition: width 0.3s ease;">
                    {current}/{total}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


