"""포인트 관련 서비스"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
from .base_service import BaseService


class PointsService(BaseService):
    """사용자 포인트 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("user_points_data.json")
    
    def get_user_points(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자의 포인트 정보를 조회합니다."""
        return self.get_by_id("user_id", user_id)
    
    def get_total_points(self, user_id: str) -> int:
        """사용자의 총 포인트를 반환합니다."""
        user_points = self.get_user_points(user_id)
        return user_points.get("total_points", 0) if user_points else 0
    
    def initialize_user_points(self, user_id: str) -> bool:
        """사용자 포인트를 초기화합니다."""
        if self.get_user_points(user_id):
            return False  # 이미 존재
        
        new_user_points = {
            "user_id": user_id,
            "total_points": 0,
            "earned_points": 0,
            "spent_points": 0,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "points_history": []
        }
        return self.create(new_user_points)
    
    def add_points(self, user_id: str, amount: int, source: str, description: str) -> bool:
        """포인트를 추가합니다."""
        user_points = self.get_user_points(user_id)
        if not user_points:
            # 사용자 포인트가 없으면 초기화
            if not self.initialize_user_points(user_id):
                return False
            user_points = self.get_user_points(user_id)
        
        transaction_id = f"tx_{uuid.uuid4().hex[:8]}"
        transaction = {
            "transaction_id": transaction_id,
            "amount": amount,
            "type": "earned",
            "source": source,
            "description": description,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        user_points["total_points"] = user_points.get("total_points", 0) + amount
        user_points["earned_points"] = user_points.get("earned_points", 0) + amount
        user_points["last_updated"] = datetime.utcnow().isoformat() + "Z"
        user_points["points_history"].append(transaction)
        
        return self.update("user_id", user_id, user_points)
    
    def spend_points(self, user_id: str, amount: int, source: str, description: str) -> bool:
        """포인트를 차감합니다."""
        user_points = self.get_user_points(user_id)
        if not user_points:
            return False
        
        current_points = user_points.get("total_points", 0)
        if current_points < amount:
            return False  # 포인트 부족
        
        transaction_id = f"tx_{uuid.uuid4().hex[:8]}"
        transaction = {
            "transaction_id": transaction_id,
            "amount": -amount,
            "type": "spent",
            "source": source,
            "description": description,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        user_points["total_points"] = current_points - amount
        user_points["spent_points"] = user_points.get("spent_points", 0) + amount
        user_points["last_updated"] = datetime.utcnow().isoformat() + "Z"
        user_points["points_history"].append(transaction)
        
        return self.update("user_id", user_id, user_points)
    
    def get_points_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """사용자의 포인트 거래 내역을 조회합니다."""
        user_points = self.get_user_points(user_id)
        if not user_points:
            return []
        
        history = user_points.get("points_history", [])
        # 최신순으로 정렬
        history.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        if limit:
            return history[:limit]
        return history
    
    def can_afford(self, user_id: str, amount: int) -> bool:
        """사용자가 특정 금액을 지불할 수 있는지 확인합니다."""
        return self.get_total_points(user_id) >= amount

