"""리더보드 관련 서비스"""
from typing import Optional, Dict, Any, List
from .base_service import BaseService


class LeaderboardService(BaseService):
    """리더보드 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("leaderboard_data.json")
    
    def get_leaderboard(self, event: str, period: str) -> List[Dict[str, Any]]:
        """특정 운동 종목과 기간의 리더보드를 조회합니다."""
        results = self.find_all(lambda l: l.get("event") == event and l.get("period") == period)
        # 점수 순으로 정렬 (높은 점수부터)
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)
    
    def get_user_rank(self, user_id: str, event: str, period: str) -> Optional[Dict[str, Any]]:
        """사용자의 특정 운동 종목과 기간의 랭킹을 조회합니다."""
        data = self.get_all()
        for entry in data:
            if (entry.get("user_id") == user_id and 
                entry.get("event") == event and 
                entry.get("period") == period):
                return entry
        return None
    
    def create_leaderboard_entry(self, event: str, period: str, user_id: str,
                                score: int, rank: int, age_group: str, gender: str) -> bool:
        """새 리더보드 항목을 생성합니다."""
        new_entry = {
            "event": event,
            "period": period,
            "user_id": user_id,
            "score": score,
            "rank": rank,
            "age_group": age_group,
            "gender": gender
        }
        return self.create(new_entry)
    
    def update_leaderboard_entry(self, user_id: str, event: str, period: str,
                                updates: Dict[str, Any]) -> bool:
        """리더보드 항목을 업데이트합니다."""
        data = self.get_all()
        for i, entry in enumerate(data):
            if (entry.get("user_id") == user_id and 
                entry.get("event") == event and 
                entry.get("period") == period):
                data[i].update(updates)
                return self._write_data(data)
        return False
    
    def update_rank(self, user_id: str, event: str, period: str, rank: int) -> bool:
        """사용자의 랭킹을 업데이트합니다."""
        return self.update_leaderboard_entry(user_id, event, period, {"rank": rank})
    
    def update_score(self, user_id: str, event: str, period: str, score: int) -> bool:
        """사용자의 점수를 업데이트합니다."""
        return self.update_leaderboard_entry(user_id, event, period, {"score": score})
    
    def get_user_leaderboards(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 모든 리더보드 항목을 조회합니다."""
        return self.find_all(lambda l: l.get("user_id") == user_id)
    
    def get_top_rankings(self, event: str, period: str, limit: int = 10) -> List[Dict[str, Any]]:
        """상위 랭킹을 조회합니다."""
        leaderboard = self.get_leaderboard(event, period)
        return leaderboard[:limit]
    
    def recalculate_ranks(self, event: str, period: str) -> bool:
        """리더보드의 랭킹을 재계산합니다."""
        leaderboard = self.get_leaderboard(event, period)
        data = self.get_all()
        
        for i, entry in enumerate(data):
            if entry.get("event") == event and entry.get("period") == period:
                # 점수로 정렬된 리더보드에서 랭크 찾기
                for rank, lb_entry in enumerate(leaderboard, 1):
                    if lb_entry.get("user_id") == entry.get("user_id"):
                        data[i]["rank"] = rank
                        break
        
        return self._write_data(data)

