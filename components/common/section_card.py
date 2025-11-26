"""섹션 카드 컴포넌트"""
import streamlit as st
from typing import Optional, Literal
from contextlib import contextmanager


class _SectionCardImpl:
    """섹션 카드 컴포넌트 - 컨텍스트 매니저로 사용 가능"""
    
    def __init__(
        self,
        title: str,
        icon: Optional[str] = None,
        variant: Literal["default", "primary", "success", "warning", "danger"] = "default",
        border_color: Optional[str] = None,
        background_color: Optional[str] = None,
        padding: str = "0.75rem",
        margin_bottom: str = "0.5rem",
        collapsible: bool = False,
        default_expanded: bool = True
    ):
        """
        섹션 카드 초기화
        
        Args:
            title: 섹션 제목
            icon: 제목 앞에 표시할 아이콘 (이모지 또는 텍스트)
            variant: 카드 스타일 변형 (default, primary, success, warning, danger)
            border_color: 왼쪽 테두리 색상 (커스텀)
            background_color: 배경색 (커스텀)
            padding: 내부 여백
            margin_bottom: 하단 여백
            collapsible: 접기/펼치기 가능 여부
            default_expanded: 기본적으로 펼쳐져 있는지 여부 (collapsible=True일 때만 적용)
        """
        self.title = title
        self.icon = icon
        self.variant = variant
        self.border_color = border_color
        self.background_color = background_color
        self.padding = padding
        self.margin_bottom = margin_bottom
        self.collapsible = collapsible
        self.default_expanded = default_expanded
        self._key = f"section_card_{hash(title)}"
        
    def _get_variant_styles(self) -> tuple[str, str, str]:
        """변형에 따른 색상 반환 (accent_color, background_color, gradient)"""
        variant_colors = {
            "default": (
                "#4c84af",  # accent
                "#f8f9fa",  # background (더 진한 회색)
                "linear-gradient(135deg, rgba(76, 132, 175, 0.12) 0%, rgba(248, 249, 250, 1) 100%)"  # gradient
            ),
            "primary": (
                "#4c84af",
                "#f0f4f8",
                "linear-gradient(135deg, rgba(76, 132, 175, 0.15) 0%, rgba(227, 242, 253, 0.5) 100%)"
            ),
            "success": (
                "#4caf50",
                "#f1f8f4",
                "linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(232, 245, 233, 0.6) 100%)"
            ),
            "warning": (
                "#ff9800",
                "#fff8f0",
                "linear-gradient(135deg, rgba(255, 152, 0, 0.15) 0%, rgba(255, 243, 224, 0.6) 100%)"
            ),
            "danger": (
                "#f44336",
                "#fff5f5",
                "linear-gradient(135deg, rgba(244, 67, 54, 0.15) 0%, rgba(255, 235, 238, 0.6) 100%)"
            ),
        }
        return variant_colors.get(self.variant, variant_colors["default"])
    
    def _render_open(self):
        """카드 시작 부분 렌더링"""
        accent_color = self.border_color or self._get_variant_styles()[0]
        bg_color = self.background_color or self._get_variant_styles()[1]
        gradient = self._get_variant_styles()[2] if not self.background_color else f"linear-gradient(135deg, {bg_color} 0%, {bg_color} 100%)"
        
        title_text = f"{self.icon} {self.title}" if self.icon else self.title
        
        # 전역 스타일 추가 (한 번만)
        if not st.session_state.get('_section_card_styles_added', False):
            st.markdown(
                """
                <style>
                .section-card-wrapper {
                    background: #f8f9fa;
                    border-radius: 12px;
                    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    border: 1px solid rgba(0, 0, 0, 0.08);
                    overflow: hidden;
                    position: relative;
                    margin-top: 1rem;
                }
                .section-card-wrapper:hover {
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 8px 24px rgba(0, 0, 0, 0.06);
                    transform: translateY(-2px);
                }
                .section-card-accent {
                    position: absolute;
                    left: 0;
                    top: 0;
                    bottom: 0;
                    width: 4px;
                    background: linear-gradient(180deg, var(--accent-color) 0%, var(--accent-color-dark) 100%);
                    border-radius: 0 4px 4px 0;
                }
                .section-card-header {
                    display: flex;
                    align-items: center;
                    padding: 0.75rem 1rem;
                    background: var(--card-gradient);
                    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
                    position: relative;
                }
                .section-card-title {
                    font-size: 1rem;
                    font-weight: 600;
                    color: #000000;
                    margin: 0;
                    letter-spacing: -0.01em;
                    line-height: 1.3;
                }
                .section-card-content {
                    padding: 1rem;
                    background: #f8f9fa;
                }
                .section-card-toggle {
                    margin-left: auto;
                    font-size: 0.75rem;
                    color: #666;
                    transition: transform 0.2s ease;
                    user-select: none;
                }
                .section-card-toggle.expanded {
                    transform: rotate(90deg);
                }
                .section-card-collapsible {
                    cursor: pointer;
                    transition: background-color 0.2s ease;
                }
                .section-card-collapsible:hover {
                    background-color: rgba(0, 0, 0, 0.02);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.session_state._section_card_styles_added = True
        
        if self.collapsible:
            # 접기/펼치기 가능한 버전
            expanded = st.session_state.get(self._key, self.default_expanded)
            toggle_icon = "▶" if not expanded else "▼"
            
            st.markdown(
                f"""
                <div class="section-card-wrapper" style="margin-bottom: {self.margin_bottom};">
                    <div class="section-card-accent" style="--accent-color: {accent_color}; --accent-color-dark: {accent_color}88;"></div>
                    <div class="section-card-header section-card-collapsible" 
                        style="--card-gradient: {gradient};"
                        onclick="document.getElementById('{self._key}_toggle').click()">
                        <h2 class="section-card-title">{title_text}</h2>
                        <span class="section-card-toggle {'expanded' if expanded else ''}" style="--accent-color: {accent_color};">
                            {toggle_icon}
                        </span>
                    </div>
                    <div id="{self._key}_content" class="section-card-content" style="{'display: block;' if expanded else 'display: none;'}">
                """,
                unsafe_allow_html=True
            )
            
            # 토글 버튼 (숨김)
            if st.button("", key=f"{self._key}_toggle", help="", use_container_width=False):
                st.session_state[self._key] = not st.session_state.get(self._key, self.default_expanded)
                st.rerun()
        else:
            # 일반 버전
            st.markdown(
                f"""
                <div class="section-card-wrapper" style="margin-bottom: {self.margin_bottom};">
                    <div class="section-card-accent" style="--accent-color: {accent_color}; --accent-color-dark: {accent_color}88;"></div>
                    <div class="section-card-header" style="--card-gradient: {gradient};">
                        <h2 class="section-card-title">{title_text}</h2>
                    </div>
                    <div class="section-card-content" style="padding: {self.padding};">
                """,
                unsafe_allow_html=True
            )
    
    def _render_close(self):
        """카드 종료 부분 렌더링"""
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self._render_open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self._render_close()
        return False


def SectionCard(title: str, **kwargs):
    """
    섹션 카드 시작 (함수 방식 - 하위 호환성)
    
    사용 예:
        SectionCard("제목")
        # 내용
        CloseSectionCard()
    
    Args:
        title: 섹션 제목
        **kwargs: _SectionCardImpl의 모든 매개변수 지원
            - icon: 아이콘 (이모지)
            - variant: 스타일 변형 (default, primary, success, warning, danger)
            - border_color: 커스텀 테두리 색상
            - background_color: 커스텀 배경색
            - padding: 내부 여백
            - margin_bottom: 하단 여백
            - collapsible: 접기/펼치기 가능 여부
            - default_expanded: 기본 펼침 상태
    """
    card = _SectionCardImpl(title, **kwargs)
    card._render_open()
    return card


def CloseSectionCard():
    """섹션 카드 종료 (함수 방식)"""
    st.markdown("</div></div>", unsafe_allow_html=True)


@contextmanager
def section_card(
    title: str,
    icon: Optional[str] = None,
    variant: Literal["default", "primary", "success", "warning", "danger"] = "default",
    **kwargs
):
    """
    섹션 카드 컨텍스트 매니저 (권장 방식)
    
    사용 예:
        with section_card("제목", icon="📋", variant="primary"):
            st.write("내용")
    
    Args:
        title: 섹션 제목
        icon: 제목 앞에 표시할 아이콘 (이모지 또는 텍스트)
        variant: 카드 스타일 변형 (default, primary, success, warning, danger)
        **kwargs: _SectionCardImpl의 추가 매개변수 지원
    """
    card = _SectionCardImpl(title, icon=icon, variant=variant, **kwargs)
    card._render_open()
    try:
        yield card
    finally:
        card._render_close()
