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
                   provider: str = "local") -> bool:
        """새 사용자를 생성합니다."""
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
        return self.create(new_user)
    
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

