import streamlit as st
from components.common.section_card import SectionCard, CloseSectionCard
from components.common.cards import FeatureCard, ExerciseCarousel
from data.constants_exercise import EXERCISES

def render(go_to):
    user_name = st.session_state.get("user_name", "체력")

    SectionCard("📖 서비스 소개")
    st.markdown("""
    **체력 FIT**은 국민체력100 프로그램을 기반으로 한 체력 측정 및 관리 서비스입니다.
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
    exercises = [
        {
            "name": e["name"],
            "description": e["description"],
            "icon": e["icon"],
            "image_path": f"assets/image/exercise/{k}.png"
        }
        for k, e in EXERCISES.items()
    ]
    ExerciseCarousel(exercises)
    CloseSectionCard()

    SectionCard("🚀 시작하기")
    st.info("💡 사이드바에서 원하는 페이지를 선택하여 시작하세요!")
    CloseSectionCard()
