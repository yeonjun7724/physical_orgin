"""서비스 레이어의 공통 베이스 클래스"""
import json
import os
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path


class BaseService:
    """JSON 파일 기반 데이터 관리의 공통 기능을 제공하는 베이스 클래스"""
    
    def __init__(self, data_file: str):
        """
        Args:
            data_file: data 폴더 내의 JSON 파일명 (예: "auth_data.json")
        """
        # 프로젝트 루트 디렉토리 찾기
        current_dir = Path(__file__).parent.parent
        self.data_dir = current_dir / "data"
        self.data_file = self.data_dir / data_file
        
        # data 디렉토리가 없으면 생성
        self.data_dir.mkdir(exist_ok=True)
    
    def _read_data(self) -> List[Dict[str, Any]]:
        """JSON 파일에서 모든 데이터를 읽어옵니다."""
        if not self.data_file.exists():
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"데이터 읽기 오류 ({self.data_file}): {e}")
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]) -> bool:
        """JSON 파일에 데이터를 씁니다."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"데이터 쓰기 오류 ({self.data_file}): {e}")
            return False
    
    def _find_by_id(self, data: List[Dict[str, Any]], id_field: str, id_value: Any) -> Optional[Dict[str, Any]]:
        """ID 필드로 데이터를 찾습니다."""
        for item in data:
            if item.get(id_field) == id_value:
                return item
        return None
    
    def _find_index_by_id(self, data: List[Dict[str, Any]], id_field: str, id_value: Any) -> int:
        """ID 필드로 데이터의 인덱스를 찾습니다."""
        for i, item in enumerate(data):
            if item.get(id_field) == id_value:
                return i
        return -1
    
    def _filter_data(self, data: List[Dict[str, Any]], filter_func: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """필터 함수를 사용하여 데이터를 필터링합니다."""
        return [item for item in data if filter_func(item)]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """모든 데이터를 반환합니다."""
        return self._read_data()
    
    def get_by_id(self, id_field: str, id_value: Any) -> Optional[Dict[str, Any]]:
        """ID로 단일 데이터를 조회합니다."""
        data = self._read_data()
        return self._find_by_id(data, id_field, id_value)
    
    def create(self, new_item: Dict[str, Any]) -> bool:
        """새 데이터를 추가합니다."""
        data = self._read_data()
        data.append(new_item)
        return self._write_data(data)
    
    def update(self, id_field: str, id_value: Any, updates: Dict[str, Any]) -> bool:
        """ID로 데이터를 업데이트합니다."""
        data = self._read_data()
        index = self._find_index_by_id(data, id_field, id_value)
        
        if index == -1:
            return False
        
        # 기존 데이터에 업데이트 내용 병합
        data[index].update(updates)
        return self._write_data(data)
    
    def delete(self, id_field: str, id_value: Any) -> bool:
        """ID로 데이터를 삭제합니다."""
        data = self._read_data()
        index = self._find_index_by_id(data, id_field, id_value)
        
        if index == -1:
            return False
        
        data.pop(index)
        return self._write_data(data)
    
    def find_all(self, filter_func: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """조건에 맞는 모든 데이터를 반환합니다."""
        data = self._read_data()
        return self._filter_data(data, filter_func)

