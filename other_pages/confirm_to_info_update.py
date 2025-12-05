"""내정보 수정 비밀번호 확인 페이지"""
import streamlit as st
from components.common.section_card import SectionCard, CloseSectionCard


def render(go_to):
   """비밀번호 확인 페이지 렌더링"""
   SectionCard("🔐 비밀번호 확인")
   
   st.markdown("내정보를 수정하려면 비밀번호 확인이 필요합니다.")
   
   password = st.text_input(
      "비밀번호",
      type="password",
      placeholder="비밀번호를 입력하세요",
      key="confirm_password_input"
   )
   
   col1, col2 = st.columns(2)
   
   with col1:
      if st.button("확인", type="primary", use_container_width=True):
         # 비밀번호 검증 (현재는 검증 없이 통과)
         # 실제로는 데이터베이스나 세션에서 비밀번호를 확인해야 함
         if password:
            # 비밀번호 확인 성공
            st.session_state.info_update_verified = True
            st.success("비밀번호가 확인되었습니다!")
            st.switch_page("other_pages/info_update.py")
         else:
            st.error("비밀번호를 입력해주세요.")
   
   with col2:
      if st.button("취소", use_container_width=True):
         st.switch_page("pages/06_setting.py")
   
   CloseSectionCard()


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

