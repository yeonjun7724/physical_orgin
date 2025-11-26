"""측정 결과 관련 서비스"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_service import BaseService


class ResultService(BaseService):
    """측정 결과 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("result_data.json")
    
    def get_result_by_id(self, result_id: str) -> Optional[Dict[str, Any]]:
        """결과 ID로 측정 결과를 조회합니다."""
        return self.get_by_id("result_id", result_id)
    
    def get_result_by_session_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 ID로 측정 결과를 조회합니다."""
        data = self.get_all()
        for result in data:
            if result.get("session_id") == session_id:
                return result
        return None
    
    def create_result(self, result_id: str, session_id: str, user_id: str, event: str,
                     raw_score: int, official_grade: str, percentile: int, tip: str,
                     frames_analyzed: int, accuracy: float, speed: int,
                     model_version: str = "v1.2.0") -> bool:
        """새 측정 결과를 생성합니다."""
        new_result = {
            "result_id": result_id,
            "session_id": session_id,
            "user_id": user_id,
            "event": event,
            "raw_score": raw_score,
            "official_grade": official_grade,
            "percentile": percentile,
            "tip": tip,
            "frames_analyzed": frames_analyzed,
            "accuracy": accuracy,
            "speed": speed,
            "model_version": model_version,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        return self.create(new_result)
    
    def update_result(self, result_id: str, updates: Dict[str, Any]) -> bool:
        """측정 결과를 업데이트합니다."""
        return self.update("result_id", result_id, updates)
    
    def get_results_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 모든 측정 결과를 조회합니다."""
        return self.find_all(lambda r: r.get("user_id") == user_id)
    
    def get_user_results_by_event(self, user_id: str, event: str) -> List[Dict[str, Any]]:
        """사용자의 특정 운동 종목 결과를 조회합니다."""
        return self.find_all(lambda r: r.get("user_id") == user_id and r.get("event") == event)
    
    def get_best_result_by_user_and_event(self, user_id: str, event: str) -> Optional[Dict[str, Any]]:
        """사용자의 특정 운동 종목 최고 기록을 조회합니다."""
        results = self.get_user_results_by_event(user_id, event)
        if not results:
            return None
        return max(results, key=lambda r: r.get("raw_score", 0))
    
    def get_results_by_grade(self, grade: str) -> List[Dict[str, Any]]:
        """등급별 측정 결과를 조회합니다."""
        return self.find_all(lambda r: r.get("official_grade") == grade)
    
    def delete_result(self, result_id: str) -> bool:
        """측정 결과를 삭제합니다."""
        return self.delete("result_id", result_id)

