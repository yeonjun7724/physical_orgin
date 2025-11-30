"""인증 관련 서비스"""
from typing import Optional, Dict, Any
from datetime import datetime
from .base_service import BaseService


class AuthService(BaseService):
    """사용자 인증 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("auth_data.json")  # 이미 _data가 있음
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자 ID로 사용자 정보를 조회합니다."""
        return self.get_by_id("id", user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """이메일로 사용자 정보를 조회합니다."""
        data = self.get_all()
        for user in data:
            if user.get("email") == email:
                return user
        return None
    
    def create_user(self, user_id: str, name: str, email: str, password_hash: str, 
                   provider: str = "local", 
                   nickname: str = None, gender: str = None, birth_year: int = None,
                   age_group: str = None, region: str = None, avatar: str = "👤") -> bool:
        """
        새 사용자를 생성합니다.
        auth_data.json과 profile_data.json에 모두 저장합니다.
        
        Args:
            user_id: 사용자 ID
            name: 이름
            email: 이메일
            password_hash: 비밀번호 해시
            provider: 제공자 (기본값: "local")
            nickname: 닉네임 (없으면 name 사용)
            gender: 성별 ("M" 또는 "F")
            birth_year: 출생년도
            age_group: 나이 그룹
            region: 지역
            avatar: 아바타 (기본값: "👤")
        """
        # auth_data.json에 사용자 정보 저장
        new_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_login": datetime.utcnow().isoformat() + "Z",
            "provider": provider,
            "is_active": True
        }
        auth_success = self.create(new_user)
        
        # profile_data.json에 프로필 정보 저장 (옵셔널 파라미터가 제공된 경우)
        if auth_success and (nickname is not None or gender is not None or birth_year is not None):
            from .profile_service import ProfileService
            profile_service = ProfileService()
            
            # 프로필이 이미 존재하는지 확인
            existing_profile = profile_service.get_profile_by_user_id(user_id)
            if not existing_profile:
                profile_success = profile_service.create_profile(
                    user_id=user_id,
                    nickname=nickname or name,
                    gender=gender or "M",
                    birth_year=birth_year or 1995,
                    age_group=age_group or "20-24",
                    region=region or "서울시-강남구",
                    avatar=avatar
                )
                if not profile_success:
                    # 프로필 생성 실패 시 경고만 출력 (auth는 이미 생성됨)
                    print(f"경고: 사용자 {user_id}의 프로필 생성에 실패했습니다.")
        
        return auth_success
    
    def update_last_login(self, user_id: str) -> bool:
        """사용자의 마지막 로그인 시간을 업데이트합니다."""
        return self.update("id", user_id, {
            "last_login": datetime.utcnow().isoformat() + "Z"
        })
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """사용자 정보를 업데이트합니다."""
        return self.update("id", user_id, updates)
    
    def deactivate_user(self, user_id: str) -> bool:
        """사용자를 비활성화합니다."""
        return self.update("id", user_id, {"is_active": False})
    
    def activate_user(self, user_id: str) -> bool:
        """사용자를 활성화합니다."""
        return self.update("id", user_id, {"is_active": True})
    
    def delete_user(self, user_id: str) -> bool:
        """사용자를 삭제합니다."""
        return self.delete("id", user_id)
    
    def get_all_active_users(self) -> list:
        """활성화된 모든 사용자를 반환합니다."""
        return self.find_all(lambda user: user.get("is_active", False))

