"""배지 관련 서비스"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_service import BaseService


class BadgeService(BaseService):
    """배지 정의 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("badge_data.json")
    
    def get_badge_by_id(self, badge_id: str) -> Optional[Dict[str, Any]]:
        """배지 ID로 배지를 조회합니다."""
        return self.get_by_id("badge_id", badge_id)
    
    def get_all_badges(self) -> List[Dict[str, Any]]:
        """모든 배지를 반환합니다."""
        return self.get_all()
    
    def get_badges_by_category(self, category: str) -> List[Dict[str, Any]]:
        """카테고리별 배지를 조회합니다."""
        return self.find_all(lambda b: b.get("category") == category)
    
    def create_badge(self, badge_id: str, name: str, description: str, icon: str,
                    condition: Dict[str, Any], reward: int, category: str) -> bool:
        """새 배지를 생성합니다."""
        new_badge = {
            "badge_id": badge_id,
            "name": name,
            "description": description,
            "icon": icon,
            "condition": condition,
            "reward": reward,
            "category": category
        }
        return self.create(new_badge)


class UserBadgeService(BaseService):
    """사용자 배지 획득 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("user_badges_data.json")
    
    def get_user_badges(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자가 획득한 모든 배지를 조회합니다."""
        return self.find_all(lambda ub: ub.get("user_id") == user_id)
    
    def has_badge(self, user_id: str, badge_id: str) -> bool:
        """사용자가 특정 배지를 보유하고 있는지 확인합니다."""
        data = self.get_all()
        for user_badge in data:
            if (user_badge.get("user_id") == user_id and 
                user_badge.get("badge_id") == badge_id):
                return True
        return False
    
    def earn_badge(self, user_id: str, badge_id: str, is_displayed: bool = False) -> bool:
        """사용자에게 배지를 부여합니다."""
        if self.has_badge(user_id, badge_id):
            return False  # 이미 보유한 배지
        
        new_user_badge = {
            "user_id": user_id,
            "badge_id": badge_id,
            "earned_at": datetime.utcnow().isoformat() + "Z",
            "is_displayed": is_displayed
        }
        return self.create(new_user_badge)
    
    def update_display_status(self, user_id: str, badge_id: str, is_displayed: bool) -> bool:
        """배지 표시 상태를 업데이트합니다."""
        data = self.get_all()
        for i, user_badge in enumerate(data):
            if (user_badge.get("user_id") == user_id and 
                user_badge.get("badge_id") == badge_id):
                data[i]["is_displayed"] = is_displayed
                return self._write_data(data)
        return False
    
    def get_displayed_badges(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자가 표시 중인 배지를 조회합니다."""
        return self.find_all(lambda ub: ub.get("user_id") == user_id and ub.get("is_displayed", False))
    
    def remove_badge(self, user_id: str, badge_id: str) -> bool:
        """사용자의 배지를 제거합니다."""
        data = self.get_all()
        for i, user_badge in enumerate(data):
            if (user_badge.get("user_id") == user_id and 
                user_badge.get("badge_id") == badge_id):
                data.pop(i)
                return self._write_data(data)
        return False

