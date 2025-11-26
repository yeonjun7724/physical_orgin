"""등급 기준표 관련 서비스"""
from typing import Optional, Dict, Any, List
from .base_service import BaseService


class ScoreTableService(BaseService):
    """등급 기준표 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("score_table_data.json")
    
    def get_score_table(self, age_group: str, gender: str, event: str) -> Optional[Dict[str, Any]]:
        """나이 그룹, 성별, 운동 종목으로 등급 기준표를 조회합니다."""
        data = self.get_all()
        for table in data:
            if (table.get("age_group") == age_group and 
                table.get("gender") == gender and 
                table.get("event") == event):
                return table
        return None
    
    def get_all_score_tables(self) -> List[Dict[str, Any]]:
        """모든 등급 기준표를 반환합니다."""
        return self.get_all()
    
    def get_score_tables_by_event(self, event: str) -> List[Dict[str, Any]]:
        """운동 종목별 등급 기준표를 조회합니다."""
        return self.find_all(lambda t: t.get("event") == event)
    
    def get_score_tables_by_age_group(self, age_group: str) -> List[Dict[str, Any]]:
        """나이 그룹별 등급 기준표를 조회합니다."""
        return self.find_all(lambda t: t.get("age_group") == age_group)
    
    def calculate_grade(self, age_group: str, gender: str, event: str, raw_score: int) -> str:
        """원점수로 등급을 계산합니다."""
        table = self.get_score_table(age_group, gender, event)
        if not table:
            return "5등급"
        
        if raw_score >= table.get("grade_1", 0):
            return "1등급"
        elif raw_score >= table.get("grade_2", 0):
            return "2등급"
        elif raw_score >= table.get("grade_3", 0):
            return "3등급"
        elif raw_score >= table.get("grade_4", 0):
            return "4등급"
        else:
            return "5등급"
    
    def create_score_table(self, age_group: str, gender: str, event: str,
                          grade_1: int, grade_2: int, grade_3: int, grade_4: int, grade_5: int,
                          source_version: str = "2024.05 공식표") -> bool:
        """새 등급 기준표를 생성합니다."""
        new_table = {
            "age_group": age_group,
            "gender": gender,
            "event": event,
            "grade_1": grade_1,
            "grade_2": grade_2,
            "grade_3": grade_3,
            "grade_4": grade_4,
            "grade_5": grade_5,
            "source_version": source_version
        }
        return self.create(new_table)
    
    def update_score_table(self, age_group: str, gender: str, event: str,
                          updates: Dict[str, Any]) -> bool:
        """등급 기준표를 업데이트합니다."""
        data = self.get_all()
        for i, table in enumerate(data):
            if (table.get("age_group") == age_group and 
                table.get("gender") == gender and 
                table.get("event") == event):
                data[i].update(updates)
                return self._write_data(data)
        return False

