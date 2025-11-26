"""계정 설정 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common import PageHeader
from components.common.section_card import SectionCard, CloseSectionCard

# 공통 설정 적용
setup_common()


def render(go_to):
   """계정 설정 페이지 렌더링"""
   PageHeader("계정 설정", "비밀번호 변경 및 계정 삭제를 관리하세요.", "🔐")
   
   # 비밀번호 변경
   SectionCard("🔑 비밀번호 변경")
   
   st.markdown("### 비밀번호 변경")
   col1, col2, col3 = st.columns(3)
   
   with col1:
      current_password = st.text_input(
         "현재 비밀번호",
         type="password",
         key="account_current_password"
      )
   
   with col2:
      new_password = st.text_input(
         "새 비밀번호",
         type="password",
         key="account_new_password"
      )
   
   with col3:
      confirm_password = st.text_input(
         "비밀번호 확인",
         type="password",
         key="account_confirm_password"
      )
   
   if st.button("비밀번호 변경", use_container_width=True, type="primary"):
      if not current_password or not new_password or not confirm_password:
         st.error("모든 필드를 입력해주세요.")
      elif new_password != confirm_password:
         st.error("새 비밀번호와 확인 비밀번호가 일치하지 않습니다.")
      else:
         st.success("비밀번호가 변경되었습니다!")
   
   CloseSectionCard()
   
   # 계정 삭제
   SectionCard("⚠️ 계정 삭제")
   
   st.markdown("### 계정 삭제")
   st.warning("⚠️ 계정을 삭제하면 모든 데이터가 영구적으로 삭제되며 복구할 수 없습니다.")
   
   if st.button("계정 삭제", use_container_width=True, type="secondary"):
      st.error("계정 삭제 기능은 준비 중입니다. 고객센터로 문의해주세요.")
   
   CloseSectionCard()
   
   # 뒤로가기 버튼
   if st.button("← 설정으로 돌아가기", use_container_width=True):
      st.switch_page("pages/06_setting.py")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

