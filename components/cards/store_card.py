"""상점 아이템 카드 컴포넌트"""
import streamlit as st
from service import InventoryService, PurchaseService, PointsService


def StoreItemCard(name: str, price: int, icon: str, description: str, 
                owned: bool = False, category: str = "아바타", item_index: int = 0):
    """
    상점 아이템 카드 컴포넌트 (Streamlit 기본 기능 사용)
    
    사용 위치:
    - pages/05_store.py: 상점 페이지의 아이템 표시
    
    사용 예시:
        StoreItemCard(
            name="기본 아바타",
            price=0,
            icon="👤",
            description="기본 제공 아바타",
            owned=True,
            category="아바타",
            item_index=0
        )
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    
    inventory_service = InventoryService()
    purchase_service = PurchaseService()
    points_service = PointsService()
    
    # 보관함에 있는지 확인
    is_in_storage = inventory_service.has_item(user_id, name) or owned
    
    # 착용 중인지 확인
    equipped_item = inventory_service.get_equipped_item(user_id, category)
    is_equipped = equipped_item and equipped_item.get("item_name") == name
    
    # 현재 포인트 확인
    current_points = points_service.get_total_points(user_id)
    can_afford = points_service.can_afford(user_id, price)
    
    # 버튼 텍스트 및 비활성화 상태 결정
    if is_equipped:
        button_text = "착용 중"
        button_disabled = True
        show_price = False
    elif is_in_storage:
        button_text = "보유 중"
        button_disabled = True
        show_price = False
    else:
        button_text = "구매"
        # 포인트가 부족하면 버튼 비활성화
        button_disabled = not can_afford
        show_price = True
    
    # 카드 컨테이너
    with st.container():
        # 아이콘과 제목
        col_icon, col_info = st.columns([1, 3])
        with col_icon:
            st.markdown(f"## {icon}")
        with col_info:
            st.markdown(f"### {name}")
            
            # description과 price를 같은 row에 배치
            col_desc, col_price = st.columns([2, 1])
            with col_desc:
                st.caption(description)
            with col_price:
                if show_price:
                    st.markdown(
                        f"""
                        <div style="font-size: 1.3rem; font-weight: 700; color: #4c84af; 
                                    display: flex; align-items: center; height: 100%;">
                            {price} FIT
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    # 버튼은 컨테이너 밖에서 전체 너비로 배치
    button_key = f"buy_{category}_{name}_{item_index}"
    button_clicked = st.button(button_text, key=button_key, use_container_width=True, disabled=button_disabled)
    
    # 구매 버튼 클릭 처리
    if button_clicked:
        if not is_in_storage:
            # 포인트 확인
            if points_service.can_afford(user_id, price):
                # 구매 처리
                purchase_id = purchase_service.create_purchase(
                    user_id, name, category, icon, price, "FIT"
                )
                
                if purchase_id:
                    # 인벤토리에 추가
                    inventory_service.add_item(
                        user_id, name, category, icon, description, price, "purchase"
                    )
                    
                    # 포인트 차감
                    points_service.spend_points(
                        user_id, price, "purchase", f"{name} 구매"
                    )
                    
                    # session_state 업데이트
                    st.session_state.user_points = points_service.get_total_points(user_id)
                    
                    st.success(f"{name}을(를) {price} FIT로 구매했습니다! 보관함에서 확인하세요.")
                    st.rerun()
                else:
                    st.error("구매 처리 중 오류가 발생했습니다.")
            else:
                current_points = points_service.get_total_points(user_id)
                st.error(f"포인트가 부족합니다. (보유: {current_points} FIT, 필요: {price} FIT)")
        
        st.markdown("---")


def StoreItemGrid(items: list, category: str = "아바타"):
    """
    상점 아이템 그리드 컴포넌트 (2열 레이아웃)
    
    사용 위치:
    - pages/05_store.py: 상점 페이지의 아이템 목록 표시
    
    사용 예시:
        items = [
            {"name": "기본 아바타", "price": 0, "icon": "👤", "desc": "기본 제공 아바타", "owned": True},
            {"name": "운동맨", "price": 500, "icon": "💪", "desc": "근육질 아바타", "owned": False},
        ]
        StoreItemGrid(items, category="아바타")
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    
    # 2열 그리드로 배치
    for i in range(0, len(items), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            item = items[i]
            StoreItemCard(
                name=item["name"],
                price=item["price"],
                icon=item["icon"],
                description=item["desc"],
                owned=item.get("owned", False),
                category=category,
                item_index=i
            )
        
        with col2:
            if i + 1 < len(items):
                item = items[i + 1]
                StoreItemCard(
                    name=item["name"],
                    price=item["price"],
                    icon=item["icon"],
                    description=item["desc"],
                    owned=item.get("owned", False),
                    category=category,
                    item_index=i + 1
                )

