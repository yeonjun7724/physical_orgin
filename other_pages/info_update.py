"""내정보 수정 페이지"""
import streamlit as st
from components.common import ProfileAvatar
from components.common.section_card import SectionCard, CloseSectionCard
from service import ProfileService
from utils.page_utils import get_user_id

def render_info_update_content(go_to=None):
  """내정보 수정 내용 렌더링 (토글로 사용 가능)"""
  # 비밀번호 검증 확인 (페이지 내부에서 처리)
  if not st.session_state.get("info_update_verified", False):
    st.warning("비밀번호 확인이 필요합니다.")
    if st.button("설정으로 돌아가기", use_container_width=True, key="go_to_setting"):
      if go_to:
        go_to("setting")
      else:
        st.rerun()
    return
  
  user_id = get_user_id()
  if not user_id:
    st.warning("로그인이 필요합니다.")
    return
  
  # ProfileService를 사용하여 프로필 정보 가져오기
  profile_service = ProfileService()
  profile = profile_service.get_profile_by_user_id(user_id)
  
  if not profile:
    st.warning("프로필 정보가 없습니다.")
    return
  
  # 프로필에서 초기값 가져오기
  current_username = profile.get("nickname", st.session_state.get("user_name", "체력"))
  current_age_group = profile.get("age_group", "20-24")
  current_gender = profile.get("gender", "M")
  current_height = profile.get("height")
  current_weight = profile.get("weight")
  
  # 나이 그룹을 표시 형식으로 변환 (20-24 -> 20대)
  age_group_display_map = {
    "10-19": "10대",
    "20-24": "20대",
    "25-29": "30대",
    "30-34": "30대",
    "35-39": "40대",
    "40-44": "40대",
    "45-49": "50대",
    "50-54": "50대",
    "55-59": "60대 이상",
    "60+": "60대 이상"
  }
  
  # 나이 그룹 표시 형식으로 변환
  age_group_display = age_group_display_map.get(current_age_group, "20대")
  
  # 성별 표시 형식으로 변환
  gender_display = "남성" if current_gender == "M" else "여성"
  
  # 프로필 설정
  SectionCard("👤 프로필 정보 수정")
  
  col1, col2 = st.columns([1, 2])
  
  with col1:
    ProfileAvatar(
      current_username,
      age_group_display,
      gender_display,
      level=100
    )
    if st.button("프로필 사진 변경", use_container_width=True):
      st.info("프로필 사진 변경 기능은 준비 중입니다.")
  
  with col2:
    st.markdown("### 기본 정보")
    
    # 닉네임 입력
    user_name = st.text_input(
        "닉네임",
        value=current_username,
        key="info_update_user_name",
        help="다른 사용자들에게 표시될 닉네임입니다"
    )
    
    col_age, col_gender = st.columns(2)
    with col_age:
        age_group_options = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
        age_group_index = age_group_options.index(age_group_display) if age_group_display in age_group_options else 1
        age_group = st.selectbox(
          "연령대",
          age_group_options,
          index=age_group_index,
          key="info_update_age_group",
          help="연령대별 통계에 사용됩니다"
        )
    
    with col_gender:
        gender_options = ["남성", "여성", "기타"]
        gender_index = gender_options.index(gender_display) if gender_display in gender_options else 0
        gender = st.selectbox(
          "성별",
          gender_options,
          index=gender_index,
          key="info_update_gender",
          help="성별별 통계에 사용됩니다"
        )
    
    height = st.number_input(
        "키 (cm)",
        min_value=100,
        max_value=250,
        value=current_height if current_height is not None else 175,
        key="info_update_height",
        help="체력 측정 결과 계산에 사용됩니다"
    )
    
    weight = st.number_input(
        "몸무게 (kg)",
        min_value=30,
        max_value=200,
        value=current_weight if current_weight is not None else 70,
        key="info_update_weight",
        help="체력 측정 결과 계산에 사용됩니다"
    )
    
    if st.button("프로필 저장", type="primary", use_container_width=True):
        # 나이 그룹을 저장 형식으로 변환 (20대 -> 20-24)
        age_group_map = {
            "10대": "10-19",
            "20대": "20-24",
            "30대": "30-34",
            "40대": "40-44",
            "50대": "50-54",
            "60대 이상": "60+"
        }
        age_group_save = age_group_map.get(age_group, "20-24")
        
        # 성별을 저장 형식으로 변환
        gender_save = "M" if gender == "남성" else ("F" if gender == "여성" else "M")
        
        # ProfileService를 사용하여 profile_data.json에 저장
        profile_updates = {
            "nickname": user_name,
            "age_group": age_group_save,
            "gender": gender_save,
            "height": height,
            "weight": weight
        }
        
        profile_success = profile_service.update_profile(user_id, profile_updates)
        
        # AuthService를 사용하여 auth_data.json의 name 필드도 업데이트
        from service import AuthService
        auth_service = AuthService()
        auth_updates = {
            "name": user_name
        }
        auth_success = auth_service.update_user(user_id, auth_updates)
        
        if profile_success and auth_success:
            # session_state도 업데이트 (호환성을 위해)
            st.session_state.user_name = user_name
            st.session_state.user_age = age_group
            st.session_state.user_gender = gender
            st.session_state.user_height = height
            st.session_state.user_weight = weight
            st.session_state.info_update_verified = False  # 검증 상태 초기화
            st.success("프로필이 저장되었습니다!")
            # 설정 페이지로 이동
            if go_to:
                go_to("setting")
            else:
                st.rerun()
        else:
            st.error("프로필 저장 중 오류가 발생했습니다.")
  
  CloseSectionCard()
  
  # 계정 삭제
  SectionCard("⚠️ 계정 삭제")
  st.warning("⚠️ 계정을 삭제하면 모든 데이터가 영구적으로 삭제되며 복구할 수 없습니다.")
  
  # 계정 삭제 확인 상태
  if "account_delete_confirm" not in st.session_state:
    st.session_state["account_delete_confirm"] = False
  
  if not st.session_state["account_delete_confirm"]:
    if st.button("계정 삭제", use_container_width=True, type="secondary", key="delete_account_btn"):
      st.session_state["account_delete_confirm"] = True
      st.rerun()
  else:
    st.error("⚠️ 정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다!")
    confirm_text = st.text_input(
      "계정 삭제를 확인하려면 '삭제'를 입력하세요",
      key="delete_confirm_text"
    )
    
    col1, col2 = st.columns(2)
    with col1:
      if st.button("삭제 확인", use_container_width=True, type="primary", key="confirm_delete_btn"):
        if confirm_text == "삭제":
          # 계정 삭제 실행
          success = _delete_user_account(user_id)
          if success:
            st.success("계정이 삭제되었습니다.")
            # 세션 초기화 및 로그아웃
            st.session_state.clear()
            if go_to:
              go_to("login")
            else:
              st.rerun()
          else:
            st.error("계정 삭제 중 오류가 발생했습니다.")
        else:
          st.error("'삭제'를 정확히 입력해주세요.")
    
    with col2:
      if st.button("취소", use_container_width=True, key="cancel_delete_btn"):
        st.session_state["account_delete_confirm"] = False
        st.rerun()
  
  CloseSectionCard()


def _delete_user_account(user_id: str) -> bool:
  """사용자 계정과 관련된 모든 데이터를 삭제합니다."""
  import json
  from pathlib import Path
  
  try:
    # 프로젝트 루트 디렉토리 찾기
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "data"
    
    # 1. auth_data.json - "id" 필드로 삭제
    from service import AuthService
    auth_service = AuthService()
    auth_service.delete_user(user_id)
    
    # 2. profile_data.json - "user_id" 필드로 삭제
    from service import ProfileService
    profile_service = ProfileService()
    profile_service.delete_profile(user_id)
    
    # 3. result_data.json - "user_id" 필드로 삭제 (results 배열 안)
    result_file = data_dir / "result_data.json"
    if result_file.exists():
      with open(result_file, 'r', encoding='utf-8') as f:
        result_data = json.load(f)
        if "results" in result_data:
          result_data["results"] = [r for r in result_data["results"] if r.get("user_id") != user_id]
          with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    # 4. measurement_data.json - "user_id" 필드로 삭제 (sessions 배열 안)
    measurement_file = data_dir / "measurement_data.json"
    if measurement_file.exists():
      with open(measurement_file, 'r', encoding='utf-8') as f:
        measurement_data = json.load(f)
        if "sessions" in measurement_data:
          measurement_data["sessions"] = [s for s in measurement_data["sessions"] if s.get("user_id") != user_id]
          with open(measurement_file, 'w', encoding='utf-8') as f:
            json.dump(measurement_data, f, ensure_ascii=False, indent=2)
    
    # 5. user_points_data.json - "user_id" 필드로 삭제
    from service import PointsService
    points_service = PointsService()
    points_data = points_service.get_all()
    points_data = [p for p in points_data if p.get("user_id") != user_id]
    points_service._write_data(points_data)
    
    # 6. daily_streak_data.json - "user_id" 필드로 삭제
    from service import StreakService
    streak_service = StreakService()
    streak_service.delete("user_id", user_id)
    
    # 7. user_badges_data.json - "user_id" 필드로 삭제 (여러 개일 수 있음)
    from service.badge_service import UserBadgeService
    badge_service = UserBadgeService()
    user_badges = badge_service.get_user_badges(user_id)
    for badge in user_badges:
      badge_service.remove_badge(user_id, badge.get("badge_id"))
    
    # 8. inventory_data.json - "user_id" 필드로 삭제 (여러 개일 수 있음)
    from service.purchase_service import InventoryService
    inventory_service = InventoryService()
    user_items = inventory_service.get_user_inventory(user_id)
    for item in user_items:
      inventory_service.remove_item(user_id, item.get("item_name"))
    
    # 9. notification_settings_data.json - "user_id" 필드로 삭제
    from service import NotificationService
    notification_service = NotificationService()
    notification_service.delete("user_id", user_id)
    
    return True
  except Exception as e:
    print(f"계정 삭제 오류: {e}")
    return False

def render(go_to):
  """내정보 수정 페이지 렌더링 (독립 페이지로 사용)"""
  render_info_update_content(go_to)
  
  # 뒤로가기 버튼
  col1, col2 = st.columns(2)
  with col1:
    if st.button("← 설정으로 돌아가기", use_container_width=True):
        st.session_state.info_update_verified = False  # 검증 상태 초기화
        go_to("setting")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

