"""인증 유틸리티"""
import streamlit as st
from service import AuthService, ProfileService
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_authenticated() -> bool:
    """사용자가 로그인되어 있는지 확인"""
    return st.session_state.get("authenticated", False)


def login_user(identifier: str, password: str):
    """
    이메일 또는 username(user_id 기반)으로 로그인
    반드시 비밀번호가 일치해야 로그인 성공
    """
    auth_service = AuthService()

    # 1) 이메일로 찾기
    user = auth_service.get_user_by_email(identifier)

    # 2) 이메일 없으면 user_id(username 기반)
    if not user:
        user_id = f"user_{identifier.lower().replace(' ', '_')}"
        user = auth_service.get_user_by_id(user_id)

    # 3) 사용자 없음
    if not user:
        return False, "존재하지 않는 계정입니다."

    # 4) 비활성 사용자
    if not user.get("is_active", True):
        return False, "비활성화된 계정입니다."

    # 5) 비밀번호 검증
    if user.get("password_hash") != hash_password(password):
        return False, "비밀번호가 일치하지 않습니다."

    # 6) 로그인 성공 처리
    st.session_state.authenticated = True
    st.session_state.user_id = user.get("id")
    st.session_state.user_name = user.get("name")

    auth_service.update_last_login(user.get("id"))

    # 프로필 없으면 자동 생성
    profile_service = ProfileService()
    profile = profile_service.get_profile_by_user_id(user.get("id"))
    if not profile:
        profile_service.create_profile(
            user_id=user.get("id"),
            nickname=user.get("name"),
            gender="M",
            birth_year=1995,
            age_group="20-24",
            region="서울시-강남구",
            avatar="👤"
        )

    return True, "로그인 성공"

def get_current_user() -> dict:
    """현재 로그인한 사용자 정보 반환"""
    return {
        "user_id": st.session_state.get("user_id"),
        "user_name": st.session_state.get("user_name"),
        "authenticated": is_authenticated()
    }
