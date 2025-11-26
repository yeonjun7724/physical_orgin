"""인증 유틸리티"""
import streamlit as st
from service import AuthService, ProfileService


def is_authenticated() -> bool:
    """사용자가 로그인되어 있는지 확인"""
    return st.session_state.get("authenticated", False)


def login_user(username: str, email: str = None, password: str = None):
    """사용자 로그인 처리"""
    auth_service = AuthService()
    
    # 이메일로 사용자 찾기 (이메일이 제공된 경우)
    user = None
    if email:
        user = auth_service.get_user_by_email(email)
    
    # 사용자명으로 사용자 찾기 (이메일로 못 찾은 경우)
    if not user:
        # 간단한 로그인: 사용자명을 user_id로 사용
        user_id = f"user_{username.lower().replace(' ', '_')}"
        user = auth_service.get_user_by_id(user_id)
        
        # 사용자가 없으면 생성
        if not user:
            auth_service.create_user(
                user_id=user_id,
                name=username,
                email=email or f"{user_id}@example.com",
                password_hash="",  # 간단한 로그인에서는 비밀번호 해시 없음
                provider="local"
            )
            user = auth_service.get_user_by_id(user_id)
    
    if user and user.get("is_active", True):
        st.session_state.authenticated = True
        st.session_state.user_id = user.get("id")
        st.session_state.user_name = user.get("name", username)
        
        # 마지막 로그인 시간 업데이트
        auth_service.update_last_login(user.get("id"))
        
        # 프로필이 없으면 기본 프로필 생성
        profile_service = ProfileService()
        profile = profile_service.get_profile_by_user_id(user.get("id"))
        if not profile:
            profile_service.create_profile(
                user_id=user.get("id"),
                nickname=username,
                gender="M",
                birth_year=1995,
                age_group="20-24",
                region="서울시-강남구",
                avatar="👤"
            )


def require_auth():
    """인증이 필요한 경우 로그인 페이지로 리다이렉트"""
    if not is_authenticated():
        return False
    return True


def get_current_user() -> dict:
    """현재 로그인한 사용자 정보 반환"""
    return {
        "user_id": st.session_state.get("user_id"),
        "user_name": st.session_state.get("user_name", "체력왕"),
        "authenticated": is_authenticated()
    }

