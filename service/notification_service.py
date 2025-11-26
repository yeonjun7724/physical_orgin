"""알림 설정 관련 서비스"""
from typing import Optional, Dict, Any
from datetime import datetime
from .base_service import BaseService


class NotificationService(BaseService):
    """알림 설정 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("notification_settings_data.json")
    
    def get_user_settings(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자의 알림 설정을 조회합니다."""
        return self.get_by_id("user_id", user_id)
    
    def initialize_settings(self, user_id: str) -> bool:
        """사용자의 알림 설정을 초기화합니다."""
        if self.get_user_settings(user_id):
            return False  # 이미 존재
        
        default_settings = {
            "user_id": user_id,
            "push_enabled": True,
            "email_enabled": True,
            "notification_types": {
                "measurement_reminder": {
                    "enabled": True,
                    "time": "09:00",
                    "frequency": "daily"
                },
                "streak_reminder": {
                    "enabled": True,
                    "time": "20:00",
                    "frequency": "daily"
                },
                "badge_earned": {
                    "enabled": True
                },
                "ranking_update": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "new_challenge": {
                    "enabled": True
                },
                "points_earned": {
                    "enabled": True
                }
            },
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        return self.create(default_settings)
    
    def update_settings(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """알림 설정을 업데이트합니다."""
        updates["updated_at"] = datetime.utcnow().isoformat() + "Z"
        return self.update("user_id", user_id, updates)
    
    def enable_push(self, user_id: str) -> bool:
        """푸시 알림을 활성화합니다."""
        return self.update("user_id", user_id, {"push_enabled": True})
    
    def disable_push(self, user_id: str) -> bool:
        """푸시 알림을 비활성화합니다."""
        return self.update("user_id", user_id, {"push_enabled": False})
    
    def enable_email(self, user_id: str) -> bool:
        """이메일 알림을 활성화합니다."""
        return self.update("user_id", user_id, {"email_enabled": True})
    
    def disable_email(self, user_id: str) -> bool:
        """이메일 알림을 비활성화합니다."""
        return self.update("user_id", user_id, {"email_enabled": False})
    
    def update_notification_type(self, user_id: str, notification_type: str, 
                                settings: Dict[str, Any]) -> bool:
        """특정 알림 타입의 설정을 업데이트합니다."""
        user_settings = self.get_user_settings(user_id)
        if not user_settings:
            if not self.initialize_settings(user_id):
                return False
            user_settings = self.get_user_settings(user_id)
        
        notification_types = user_settings.get("notification_types", {})
        if notification_type not in notification_types:
            notification_types[notification_type] = {}
        
        notification_types[notification_type].update(settings)
        
        return self.update("user_id", user_id, {
            "notification_types": notification_types
        })
    
    def enable_notification_type(self, user_id: str, notification_type: str) -> bool:
        """특정 알림 타입을 활성화합니다."""
        return self.update_notification_type(user_id, notification_type, {"enabled": True})
    
    def disable_notification_type(self, user_id: str, notification_type: str) -> bool:
        """특정 알림 타입을 비활성화합니다."""
        return self.update_notification_type(user_id, notification_type, {"enabled": False})
    
    def is_notification_enabled(self, user_id: str, notification_type: str) -> bool:
        """특정 알림 타입이 활성화되어 있는지 확인합니다."""
        settings = self.get_user_settings(user_id)
        if not settings:
            return False
        
        notification_types = settings.get("notification_types", {})
        notification = notification_types.get(notification_type, {})
        return notification.get("enabled", False)

