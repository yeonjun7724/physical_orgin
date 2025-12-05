"""설정 페이지"""
import streamlit as st
import re
from components.common.section_card import SectionCard, CloseSectionCard
from service import NotificationService, AuthService


def render(go_to):
   """설정 페이지 렌더링"""
   from utils.page_utils import get_user_id
   user_id = get_user_id()
   if not user_id:
      st.warning("로그인이 필요합니다.")
      return

   notification_service = NotificationService()
   user_settings = notification_service.get_user_settings(user_id)
   
   if not user_settings:
      notification_service.initialize_settings(user_id)
      user_settings = notification_service.get_user_settings(user_id)
   
   st.markdown("---")
   # 이메일 설정 섹션

   SectionCard("📧 이메일 알림 설정")
   st.markdown("알림을 받을 이메일 주소를 설정하세요.")
   # 현재 사용자 이메일 가져오기 (auth_data에서)
   auth_service = AuthService()
   current_user = auth_service.get_user_by_id(user_id)
   current_email = current_user.get("email", "") if current_user else ""
   
   # 저장된 이메일 주소 가져오기 (notification_settings에서)
   saved_email = user_settings.get("email", current_email)
   
   # 이메일 주소 입력
   email_address = st.text_input(
      "이메일 주소",
      value=saved_email,
      placeholder="example@email.com",
      key="notification_email",
      help="알림을 받을 이메일 주소를 입력하세요"
   )
   
   # 이메일 형식 검증
   email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
   is_valid_email = re.match(email_pattern, email_address) is not None if email_address else False
   
   if email_address and not is_valid_email:
      st.warning("⚠️ 올바른 이메일 형식을 입력해주세요.")
   
   # 이메일 알림 활성화/비활성화
   email_enabled = user_settings.get("email_enabled", True)
   email_notification_enabled = st.checkbox(
      "이메일 알림 받기",
      value=email_enabled,
      key="email_notification_enabled",
      help="체크하면 설정한 이메일 주소로 알림을 받습니다"
   )

   CloseSectionCard()
   st.markdown("---")
   # 알림 타입 매핑
   st.markdown("### 🔔 알림 종류 설정")
   notification_mapping = {
      "측정 완료 알림": "measurement_reminder",
      "랭킹 변동 알림": "ranking_update",
      "챌린지 알림": "new_challenge",
      "주간 리포트 알림": "weekly_report",
      "이벤트 및 프로모션": "event_promotion",
   }
   
   notification_types = user_settings.get("notification_types", {})
   updated_settings = {}
   
   for setting_name, setting_key in notification_mapping.items():
      notification = notification_types.get(setting_key, {})
      default_value = notification.get("enabled", True)
      # 고유한 key 생성 (setting_name을 기반으로)
      unique_key = f"notif_{setting_key}_{setting_name}"
      updated_settings[setting_key] = st.checkbox(
         setting_name,
         value=default_value,
         key=unique_key
      )
   
   if st.button("알림 설정 저장", use_container_width=True, type="primary"):
      # 이메일 주소 저장
      if email_address and is_valid_email:
         notification_service.update_settings(user_id, {"email": email_address})
      
      # 이메일 알림 활성화/비활성화 저장
      if email_notification_enabled:
         notification_service.enable_email(user_id)
      else:
         notification_service.disable_email(user_id)
      
      # 알림 타입 설정 저장
      for setting_key, value in updated_settings.items():
         notification_service.update_notification_type(user_id, setting_key, {"enabled": value})
      
      st.success("알림 설정이 저장되었습니다!")
      st.rerun()
   
   CloseSectionCard()
   st.markdown("---")
   # 프라이버시 설정
   SectionCard("🔒 프라이버시 설정")
   
   privacy_settings = {
      "프로필 공개": st.session_state.get("privacy_profile_public", True),
      "랭킹 공개": st.session_state.get("privacy_ranking_public", True),
      "측정 결과 공개": st.session_state.get("privacy_results_public", False),
      "활동 피드 공개": st.session_state.get("privacy_feed_public", True),
   }
   
   updated_privacy = {}
   for setting_name, default_value in privacy_settings.items():
      updated_privacy[setting_name] = st.checkbox(
         setting_name,
         value=default_value,
         key=f"privacy_{setting_name}",
         help="다른 사용자들이 내 정보를 볼 수 있는지 설정합니다"
      )
   
   data_collection = st.checkbox(
      "익명화된 데이터 수집에 동의합니다",
      value=st.session_state.get("data_collection_consent", False),
      key="data_collection_consent",
      help="서비스 개선을 위해 익명화된 데이터를 수집합니다"
   )
   
   if st.button("프라이버시 설정 저장", use_container_width=True):
      for key, value in updated_privacy.items():
         st.session_state[f"privacy_{key}"] = value
      st.session_state.data_collection_consent = data_collection
      st.success("프라이버시 설정이 저장되었습니다!")
   
   CloseSectionCard()
   
   st.markdown("---")
   # 데이터 관리
   SectionCard("📊 데이터 관리")
   col1, col2 = st.columns(2)
   
   with col1:
      # 데이터 내보내기 박스
      st.markdown(
         """
         <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; 
                     border-left: 4px solid #4c84af; margin-bottom: 1rem;">
            <h3 style="margin-top: 0;">데이터 내보내기</h3>
            <p style="color: #666; margin-bottom: 1rem;">모든 측정 데이터를 다운로드할 수 있습니다.</p>
         </div>
         """,
         unsafe_allow_html=True
      )
      if st.button("데이터 내보내기", use_container_width=True, type="primary", key="export_data"):
         st.info("데이터 내보내기 기능은 준비 중입니다. 곧 제공될 예정입니다.")
   
   with col2:
      # 데이터 삭제 박스
      st.markdown(
         """
         <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; 
                     border-left: 4px solid #f44336; margin-bottom: 1rem;">
            <h3 style="margin-top: 0;">데이터 삭제</h3>
            <p style="color: #666; margin-bottom: 1rem;">모든 측정 데이터를 삭제할 수 있습니다.</p>
         </div>
         """,
         unsafe_allow_html=True
      )
      if st.button("데이터 삭제", use_container_width=True, type="secondary", key="delete_data"):
         st.warning("⚠️ 이 작업은 되돌릴 수 없습니다!")
         confirm = st.checkbox("정말로 모든 데이터를 삭제하시겠습니까?", key="confirm_delete")
         if confirm:
            if st.button("삭제 확인", type="primary", use_container_width=True, key="confirm_delete_btn"):
               st.error("데이터 삭제 기능은 준비 중입니다.")
   
   CloseSectionCard()
   st.markdown("---")
   
   # 내정보 수정 섹션
   SectionCard("👤 내정보 수정")
   st.markdown("프로필 정보를 수정할 수 있습니다.")
   
   if st.button("내정보 수정", use_container_width=True, type="primary", key="edit_profile"):
      st.session_state["info_update_modal_open"] = True
      st.rerun()
   
   CloseSectionCard()
   st.markdown("---")
   
   # 내정보 수정 모달
   if st.session_state.get("info_update_modal_open", False):
      from components.common.modal import modal
      from other_pages.info_update import render as render_info_update
      
      with modal("👤 내정보 수정", "info_update_modal", size="large"):
         render_info_update(go_to)

