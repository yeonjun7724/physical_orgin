"""내 보관함 페이지"""
import streamlit as st
from utils.app_common import setup_common
from components.common import PageHeader
from components.common.section_card import SectionCard, CloseSectionCard
from service import InventoryService

# 공통 설정 적용
setup_common()


def render(go_to):
    """보관함 페이지 렌더링"""
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("로그인이 필요합니다.")
        return
    
    inventory_service = InventoryService()
    
    PageHeader("내 보관함", "구매한 아바타와 프레임을 확인하고 착용할 수 있습니다.", "📦")
    
    # 인벤토리에서 아이템 가져오기
    inventory = inventory_service.get_user_inventory(user_id)
    
    # 카테고리별로 분류
    avatars = [item for item in inventory if item.get("item_category") == "아바타"]
    frames = [item for item in inventory if item.get("item_category") == "프레임"]
    
    # 아바타 섹션
    SectionCard("👤 아바타")
    
    if avatars:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, avatar in enumerate(avatars):
            with cols[i % 3]:
                avatar_name = avatar.get('item_name', '')
                equipped = avatar.get('equipped', False)
                card_style = "background: #e3f2fd; border: 2px solid #4c84af;" if equipped else "background: #f8f9fa; border: 1px solid #e0e0e0;"
                
                st.markdown(
                    f"""
                    <div style="{card_style} border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{avatar.get('item_icon', '👤')}</div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">{avatar_name}</div>
                        <div style="font-size: 0.85rem; color: #666; margin-bottom: 0.5rem;">{avatar.get('item_description', '')}</div>
                        {f'<div style="color: #4c84af; font-weight: 600; font-size: 0.9rem;">✓ 착용 중</div>' if equipped else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if not equipped:
                    if st.button("착용하기", key=f"equip_avatar_{avatar_name}", use_container_width=True, type="primary"):
                        if inventory_service.equip_item(user_id, avatar_name):
                            st.success(f"{avatar_name}을(를) 착용했습니다!")
                            st.rerun()
                else:
                    st.button("착용 중", key=f"equipped_avatar_{avatar_name}", use_container_width=True, disabled=True)
    else:
        st.info("보관함에 아바타가 없습니다. 상점에서 구매해보세요!")
    
    CloseSectionCard()
    
    # 프레임 섹션
    SectionCard("🖼️ 프레임")
    
    if frames:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, frame in enumerate(frames):
            with cols[i % 3]:
                frame_name = frame.get('item_name', '')
                equipped = frame.get('equipped', False)
                card_style = "background: #e3f2fd; border: 2px solid #4c84af;" if equipped else "background: #f8f9fa; border: 1px solid #e0e0e0;"
                
                st.markdown(
                    f"""
                    <div style="{card_style} border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{frame.get('item_icon', '📄')}</div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">{frame_name}</div>
                        <div style="font-size: 0.85rem; color: #666; margin-bottom: 0.5rem;">{frame.get('item_description', '')}</div>
                        {f'<div style="color: #4c84af; font-weight: 600; font-size: 0.9rem;">✓ 착용 중</div>' if equipped else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if not equipped:
                    if st.button("착용하기", key=f"equip_frame_{frame_name}", use_container_width=True, type="primary"):
                        if inventory_service.equip_item(user_id, frame_name):
                            st.success(f"{frame_name}을(를) 착용했습니다!")
                            st.rerun()
                else:
                    st.button("착용 중", key=f"equipped_frame_{frame_name}", use_container_width=True, disabled=True)
    else:
        st.info("보관함에 프레임이 없습니다. 상점에서 구매해보세요!")
    
    CloseSectionCard()
    
    # 뒤로가기 버튼
    if st.button("← 프로필로 돌아가기", use_container_width=True):
        st.switch_page("pages/04_profile.py")


# 페이지가 직접 실행될 때 렌더링
if __name__ == "__main__" or not st.session_state.get('_rendered_by_app', False):
    from utils.page_utils import run_page
    run_page(render)

