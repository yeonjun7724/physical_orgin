"""연속 측정 관련 서비스"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .base_service import BaseService


class StreakService(BaseService):
    """연속 측정 일수 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("daily_streak_data.json")
    
    def get_user_streak(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자의 연속 측정 정보를 조회합니다."""
        return self.get_by_id("user_id", user_id)
    
    def initialize_streak(self, user_id: str) -> bool:
        """사용자의 연속 측정을 초기화합니다."""
        if self.get_user_streak(user_id):
            return False  # 이미 존재
        
        today = datetime.utcnow().date().isoformat()
        new_streak = {
            "user_id": user_id,
            "current_streak": 0,
            "longest_streak": 0,
            "last_measurement_date": None,
            "streak_start_date": None,
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        return self.create(new_streak)
    
    def update_streak(self, user_id: str) -> Dict[str, Any]:
        """
        측정 완료 시 연속 측정을 업데이트합니다.
        Returns:
            {"current_streak": int, "longest_streak": int, "is_new_streak": bool}
        """
        streak = self.get_user_streak(user_id)
        if not streak:
            self.initialize_streak(user_id)
            streak = self.get_user_streak(user_id)
        
        today = datetime.utcnow().date()
        last_date_str = streak.get("last_measurement_date")
        
        is_new_streak = False
        current_streak = streak.get("current_streak", 0)
        longest_streak = streak.get("longest_streak", 0)
        
        if last_date_str:
            last_date = datetime.fromisoformat(last_date_str).date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # 오늘 이미 측정함
                pass
            elif days_diff == 1:
                # 연속 측정 유지
                current_streak += 1
            else:
                # 연속 측정 끊김, 새로 시작
                current_streak = 1
                is_new_streak = True
                streak["streak_start_date"] = today.isoformat()
        else:
            # 첫 측정
            current_streak = 1
            is_new_streak = True
            streak["streak_start_date"] = today.isoformat()
        
        # 최장 연속 기록 업데이트
        if current_streak > longest_streak:
            longest_streak = current_streak
        
        # 업데이트
        updates = {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_measurement_date": today.isoformat(),
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        self.update("user_id", user_id, updates)
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "is_new_streak": is_new_streak
        }
    
    def get_current_streak(self, user_id: str) -> int:
        """사용자의 현재 연속 측정 일수를 반환합니다."""
        streak = self.get_user_streak(user_id)
        return streak.get("current_streak", 0) if streak else 0
    
    def get_longest_streak(self, user_id: str) -> int:
        """사용자의 최장 연속 측정 일수를 반환합니다."""
        streak = self.get_user_streak(user_id)
        return streak.get("longest_streak", 0) if streak else 0
    
    def reset_streak(self, user_id: str) -> bool:
        """연속 측정을 초기화합니다."""
        return self.update("user_id", user_id, {
            "current_streak": 0,
            "last_measurement_date": None,
            "streak_start_date": None,
            "updated_at": datetime.utcnow().isoformat() + "Z"
        })

