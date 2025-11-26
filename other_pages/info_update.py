"""내정보 수정 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common import PageHeader, ProfileAvatar
from components.common.section_card import SectionCard, CloseSectionCard

# 공통 설정 적용
setup_common()

# 비밀번호 검증 확인
if not st.session_state.get("info_update_verified", False):
  st.switch_page("other_pages/confirm_to_info_update.py")


def render(go_to):
  """내정보 수정 페이지 렌더링"""
  PageHeader("내정보 수정", "프로필 정보를 수정하세요.", "✏️")
  
  # 로그인한 username 가져오기
  current_username = st.session_state.get("user_name", "체력왕")
  
  # 프로필 설정
  SectionCard("👤 프로필 정보 수정")
  
  col1, col2 = st.columns([1, 2])
  
  with col1:
    ProfileAvatar(
      current_username,
      st.session_state.get("user_age", "20대"),
      st.session_state.get("user_gender", "남성"),
      level=100
    )
    if st.button("프로필 사진 변경", use_container_width=True):
      st.info("프로필 사진 변경 기능은 준비 중입니다.")
  
  with col2:
    st.markdown("### 기본 정보")
    
    # 로그인한 username을 기본값으로 사용
    user_name = st.text_input(
        "닉네임",
        value=current_username,
        key="info_update_user_name",
        help="다른 사용자들에게 표시될 닉네임입니다"
    )
    
    col_age, col_gender = st.columns(2)
    with col_age:
        age_group = st.selectbox(
          "연령대",
          ["10대", "20대", "30대", "40대", "50대", "60대 이상"],
          index=["10대", "20대", "30대", "40대", "50대", "60대 이상"].index(st.session_state.get("user_age", "20대")) if st.session_state.get("user_age", "20대") in ["10대", "20대", "30대", "40대", "50대", "60대 이상"] else 1,
          key="info_update_age_group",
          help="연령대별 통계에 사용됩니다"
        )
    
    with col_gender:
        gender = st.selectbox(
          "성별",
          ["남성", "여성", "기타"],
          index=["남성", "여성", "기타"].index(st.session_state.get("user_gender", "남성")) if st.session_state.get("user_gender", "남성") in ["남성", "여성", "기타"] else 0,
          key="info_update_gender",
          help="성별별 통계에 사용됩니다"
        )
    
    height = st.number_input(
        "키 (cm)",
        min_value=100,
        max_value=250,
        value=st.session_state.get("user_height", 175),
        key="info_update_height",
        help="체력 측정 결과 계산에 사용됩니다"
    )
    
    weight = st.number_input(
        "몸무게 (kg)",
        min_value=30,
        max_value=200,
        value=st.session_state.get("user_weight", 70),
        key="info_update_weight",
        help="체력 측정 결과 계산에 사용됩니다"
    )
    
    if st.button("프로필 저장", type="primary", use_container_width=True):
        st.session_state.user_name = user_name
        st.session_state.user_age = age_group
        st.session_state.user_gender = gender
        st.session_state.user_height = height
        st.session_state.user_weight = weight
        st.success("프로필이 저장되었습니다!")
        st.rerun()
  
  CloseSectionCard()
  
  # 계정 삭제
  SectionCard("⚠️ 계정 삭제")
  
  st.markdown("### 계정 삭제")
  st.warning("⚠️ 계정을 삭제하면 모든 데이터가 영구적으로 삭제되며 복구할 수 없습니다.")
  
  if st.button("계정 삭제", use_container_width=True, type="secondary"):
    st.error("계정 삭제 기능은 준비 중입니다. 고객센터로 문의해주세요.")
  
  CloseSectionCard()
  
  # 뒤로가기 버튼
  col1, col2 = st.columns(2)
  with col1:
    if st.button("← 설정으로 돌아가기", use_container_width=True):
        st.session_state.info_update_verified = False  # 검증 상태 초기화
        st.switch_page("pages/06_setting.py")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

