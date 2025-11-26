"""측정 세션 관련 서비스"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_service import BaseService


class MeasurementService(BaseService):
    """측정 세션 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("measurement_data.json")
    
    def get_measurement_by_session_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 ID로 측정 데이터를 조회합니다."""
        return self.get_by_id("session_id", session_id)
    
    def create_measurement(self, session_id: str, user_id: str, event: str,
                          device_info: Dict[str, Any], status: str = "completed") -> bool:
        """새 측정 세션을 생성합니다."""
        now = datetime.utcnow().isoformat() + "Z"
        new_measurement = {
            "session_id": session_id,
            "user_id": user_id,
            "event": event,
            "started_at": now,
            "ended_at": now,
            "device_info": device_info,
            "status": status
        }
        return self.create(new_measurement)
    
    def update_measurement(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """측정 세션을 업데이트합니다."""
        return self.update("session_id", session_id, updates)
    
    def complete_measurement(self, session_id: str) -> bool:
        """측정을 완료 상태로 업데이트합니다."""
        return self.update("session_id", session_id, {
            "status": "completed",
            "ended_at": datetime.utcnow().isoformat() + "Z"
        })
    
    def abort_measurement(self, session_id: str) -> bool:
        """측정을 중단 상태로 업데이트합니다."""
        return self.update("session_id", session_id, {
            "status": "aborted",
            "ended_at": datetime.utcnow().isoformat() + "Z"
        })
    
    def get_measurements_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 모든 측정 세션을 조회합니다."""
        return self.find_all(lambda m: m.get("user_id") == user_id)
    
    def get_completed_measurements_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 완료된 측정 세션을 조회합니다."""
        return self.find_all(lambda m: m.get("user_id") == user_id and m.get("status") == "completed")
    
    def get_measurements_by_event(self, event: str) -> List[Dict[str, Any]]:
        """운동 종목별 측정 세션을 조회합니다."""
        return self.find_all(lambda m: m.get("event") == event)
    
    def get_user_measurements_by_event(self, user_id: str, event: str) -> List[Dict[str, Any]]:
        """사용자의 특정 운동 종목 측정 세션을 조회합니다."""
        return self.find_all(lambda m: m.get("user_id") == user_id and m.get("event") == event)
    
    def delete_measurement(self, session_id: str) -> bool:
        """측정 세션을 삭제합니다."""
        return self.delete("session_id", session_id)

