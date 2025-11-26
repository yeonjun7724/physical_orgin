"""메인 앱 페이지 - 서비스 소개"""
import streamlit as st
from utils.app_common import setup_common
from utils.routes import render_page
from utils.constants import EXERCISES
from components.common.section_card import SectionCard, CloseSectionCard
from components.app import FeatureCard, ExerciseCarousel

# 공통 설정 적용 (인증 체크 포함)
setup_common()

# measure, result, signup, tutorial 페이지들은 별도 처리 (other_pages에 있음)
current_page = st.session_state.get("page", "home")
if current_page in ("measure", "result", "signup") or current_page.startswith("tutorial_"):
    render_page()
    st.stop()

# 서비스 소개 페이지 렌더링
user_name = st.session_state.get("user_name", "체력왕")
st.markdown(
    f"""
    <div style="margin-bottom: 2rem; margin-top: 1rem;">
        <p style="margin: 0; color: #666; font-size: 1.1rem;">{user_name}님, 국민체력100 서비스에 오신 것을 환영합니다!</p>
    </div>
    """,
    unsafe_allow_html=True
)

SectionCard("📖 서비스 소개")
st.markdown("""
**체력왕 FIT**은 국민체력100 프로그램을 기반으로 한 체력 측정 및 관리 서비스입니다.
""")

FeatureCard(
    icon="💪",
    title="체력 측정",
    description="6가지 종목으로 나의 체력을 정확하게 측정합니다"
)

FeatureCard(
    icon="📊",
    title="랭킹 시스템",
    description="다른 사용자들과 비교하여 나의 순위를 확인할 수 있습니다"
)

FeatureCard(
    icon="🎯",
    title="목표 관리",
    description="개인 목표를 설정하고 달성 현황을 추적합니다"
)

FeatureCard(
    icon="🏆",
    title="보상 시스템",
    description="측정 및 챌린지 완료 시 보상을 받을 수 있습니다"
)

FeatureCard(
    icon="📈",
    title="성장 추적",
    description="체력 변화를 그래프로 확인하고 성장을 체감할 수 있습니다"
)
CloseSectionCard()

SectionCard("🏋️ 측정 종목")
# EXERCISES에서 운동 데이터를 가져와서 ExerciseCarousel 형식으로 변환
exercises = [
    {
        "name": exercise_data["name"],
        "description": exercise_data["description"],
        "icon": exercise_data["icon"],
        "image_path": f"assets/image/exercise/{exercise_data['key']}.png"
    }
    for exercise_data in EXERCISES.values()
]
ExerciseCarousel(exercises)
CloseSectionCard()


SectionCard("🚀 시작하기")
st.info("💡 사이드바에서 원하는 페이지를 선택하여 시작하세요!")
CloseSectionCard()