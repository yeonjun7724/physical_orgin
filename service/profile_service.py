"""프로필 관련 서비스"""
from typing import Optional, Dict, Any
from .base_service import BaseService


class ProfileService(BaseService):
    """사용자 프로필 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("profile_data.json")
    
    def get_profile_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자 ID로 프로필을 조회합니다."""
        return self.get_by_id("user_id", user_id)
    
    def create_profile(self, user_id: str, nickname: str, gender: str, 
                    birth_year: int, age_group: str, region: str, 
                    avatar: str = "👤") -> bool:
        """새 프로필을 생성합니다."""
        new_profile = {
            "user_id": user_id,
            "nickname": nickname,
            "gender": gender,
            "birth_year": birth_year,
            "age_group": age_group,
            "region": region,
            "avatar": avatar
        }
        return self.create(new_profile)
    
    def update_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """프로필 정보를 업데이트합니다."""
        return self.update("user_id", user_id, updates)
    
    def update_nickname(self, user_id: str, nickname: str) -> bool:
        """닉네임을 업데이트합니다."""
        return self.update("user_id", user_id, {"nickname": nickname})
    
    def update_avatar(self, user_id: str, avatar: str) -> bool:
        """아바타를 업데이트합니다."""
        return self.update("user_id", user_id, {"avatar": avatar})
    
    def update_region(self, user_id: str, region: str) -> bool:
        """지역을 업데이트합니다."""
        return self.update("user_id", user_id, {"region": region})
    
    def delete_profile(self, user_id: str) -> bool:
        """프로필을 삭제합니다."""
        return self.delete("user_id", user_id)
    
    def get_profiles_by_age_group(self, age_group: str) -> list:
        """나이 그룹별 프로필을 조회합니다."""
        return self.find_all(lambda profile: profile.get("age_group") == age_group)
    
    def get_profiles_by_region(self, region: str) -> list:
        """지역별 프로필을 조회합니다."""
        return self.find_all(lambda profile: profile.get("region") == region)

