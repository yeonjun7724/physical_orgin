"""구매 관련 서비스"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
from .base_service import BaseService


class PurchaseService(BaseService):
    """구매 내역 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("purchase_history_data.json")
    
    def get_purchase_by_id(self, purchase_id: str) -> Optional[Dict[str, Any]]:
        """구매 ID로 구매 내역을 조회합니다."""
        return self.get_by_id("purchase_id", purchase_id)
    
    def get_user_purchases(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 모든 구매 내역을 조회합니다."""
        return self.find_all(lambda p: p.get("user_id") == user_id)
    
    def create_purchase(self, user_id: str, item_name: str, item_category: str,
                       item_icon: str, price: int, payment_method: str = "FIT") -> Optional[str]:
        """새 구매 내역을 생성합니다."""
        purchase_id = f"purchase_{uuid.uuid4().hex[:8]}"
        new_purchase = {
            "purchase_id": purchase_id,
            "user_id": user_id,
            "item_name": item_name,
            "item_category": item_category,
            "item_icon": item_icon,
            "price": price,
            "purchased_at": datetime.utcnow().isoformat() + "Z",
            "payment_method": payment_method
        }
        
        if self.create(new_purchase):
            return purchase_id
        return None


class InventoryService(BaseService):
    """인벤토리 데이터 관리 서비스"""
    
    def __init__(self):
        super().__init__("inventory_data.json")
    
    def get_user_inventory(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 인벤토리를 조회합니다."""
        return self.find_all(lambda item: item.get("user_id") == user_id)
    
    def get_user_items_by_category(self, user_id: str, category: str) -> List[Dict[str, Any]]:
        """사용자의 특정 카테고리 아이템을 조회합니다."""
        return self.find_all(lambda item: item.get("user_id") == user_id and item.get("item_category") == category)
    
    def has_item(self, user_id: str, item_name: str) -> bool:
        """사용자가 특정 아이템을 보유하고 있는지 확인합니다."""
        data = self.get_all()
        for item in data:
            if item.get("user_id") == user_id and item.get("item_name") == item_name:
                return True
        return False
    
    def add_item(self, user_id: str, item_name: str, item_category: str,
                item_icon: str, item_description: str, price: int,
                acquired_method: str = "purchase") -> bool:
        """인벤토리에 아이템을 추가합니다."""
        if self.has_item(user_id, item_name):
            return False  # 이미 보유한 아이템
        
        new_item = {
            "user_id": user_id,
            "item_name": item_name,
            "item_category": item_category,
            "item_icon": item_icon,
            "item_description": item_description,
            "price": price,
            "equipped": False,
            "acquired_at": datetime.utcnow().isoformat() + "Z",
            "acquired_method": acquired_method
        }
        return self.create(new_item)
    
    def equip_item(self, user_id: str, item_name: str) -> bool:
        """아이템을 착용합니다. 같은 카테고리의 다른 아이템은 자동으로 해제됩니다."""
        data = self.get_all()
        item_to_equip = None
        category = None
        
        # 착용할 아이템 찾기
        for item in data:
            if item.get("user_id") == user_id and item.get("item_name") == item_name:
                item_to_equip = item
                category = item.get("item_category")
                break
        
        if not item_to_equip:
            return False
        
        # 같은 카테고리의 다른 아이템 해제
        for item in data:
            if (item.get("user_id") == user_id and 
                item.get("item_category") == category and 
                item.get("item_name") != item_name):
                item["equipped"] = False
        
        # 착용할 아이템 장착
        for item in data:
            if item.get("user_id") == user_id and item.get("item_name") == item_name:
                item["equipped"] = True
                break
        
        return self._write_data(data)
    
    def unequip_item(self, user_id: str, item_name: str) -> bool:
        """아이템을 해제합니다."""
        data = self.get_all()
        for item in data:
            if item.get("user_id") == user_id and item.get("item_name") == item_name:
                item["equipped"] = False
                return self._write_data(data)
        return False
    
    def get_equipped_item(self, user_id: str, category: str) -> Optional[Dict[str, Any]]:
        """사용자가 착용 중인 특정 카테고리 아이템을 조회합니다."""
        items = self.get_user_items_by_category(user_id, category)
        for item in items:
            if item.get("equipped", False):
                return item
        return None
    
    def remove_item(self, user_id: str, item_name: str) -> bool:
        """인벤토리에서 아이템을 제거합니다."""
        data = self.get_all()
        for i, item in enumerate(data):
            if item.get("user_id") == user_id and item.get("item_name") == item_name:
                data.pop(i)
                return self._write_data(data)
        return False

