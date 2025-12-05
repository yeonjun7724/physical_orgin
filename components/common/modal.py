"""모달 컴포넌트"""
import streamlit as st
from contextlib import contextmanager


@contextmanager
def modal(title: str, key: str, size: str = "large"):
    """
    모달 컨텍스트 매니저
    
    사용 예시:
        with modal("제목", "modal_key"):
            st.write("모달 내용")
    
    Args:
        title: 모달 제목
        key: 모달을 열고 닫는 데 사용할 고유 키
        size: 모달 크기 ("small", "medium", "large")
    """
    # 모달 열기/닫기 상태 관리
    if f"{key}_open" not in st.session_state:
        st.session_state[f"{key}_open"] = False
    
    # 모달이 열려있지 않으면 아무것도 렌더링하지 않음
    if not st.session_state.get(f"{key}_open", False):
        # CSS만 추가
        modal_css = f"""
        <style>
        .modal-overlay-{key} {{
            display: none;
        }}
        </style>
        """
        st.markdown(modal_css, unsafe_allow_html=True)
        return
    
    # 모달 CSS
    size_width = {
        "small": ("90%", "500px"),
        "medium": ("70%", "800px"),
        "large": ("85%", "1200px")
    }
    width, max_width = size_width.get(size, ("85%", "1200px"))
    
    modal_css = f"""
    <style>
    /* 모달 오버레이 */
    .modal-overlay-{key} {{
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6);
        z-index: 9999;
        overflow-y: auto;
        padding: 20px;
        box-sizing: border-box;
    }}
    
    /* 모달 컨테이너 */
    .modal-container-{key} {{
        position: relative;
        margin: 0 auto;
        padding: 0;
        width: {width};
        max-width: {max_width};
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: modalFadeIn-{key} 0.3s ease;
    }}
    
    @keyframes modalFadeIn-{key} {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* 모달 헤더 */
    .modal-header-{key} {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        border-bottom: 2px solid #e5e5e5;
        background: linear-gradient(135deg, #4c84af 0%, #3a6a8a 100%);
        color: white;
        border-radius: 12px 12px 0 0;
    }}
    
    .modal-title-{key} {{
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .modal-close-btn-{key} {{
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        font-size: 1.8rem;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
        line-height: 1;
        padding: 0;
    }}
    
    .modal-close-btn-{key}:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    
    /* 모달 본문 */
    .modal-body-{key} {{
        padding: 1.5rem;
        max-height: calc(100vh - 200px);
        overflow-y: auto;
    }}
    </style>
    """
    
    st.markdown(modal_css, unsafe_allow_html=True)
    
    # 모달 오버레이 시작
    st.markdown(f'<div class="modal-overlay-{key}" id="modal-overlay-{key}">', unsafe_allow_html=True)
    st.markdown(f'<div class="modal-container-{key}">', unsafe_allow_html=True)
    
    # 모달 헤더
    st.markdown(
        f"""
        <div class="modal-header-{key}">
            <h2 class="modal-title-{key}">{title}</h2>
            <button class="modal-close-btn-{key}" onclick="document.getElementById('close-btn-{key}').click()">×</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 닫기 버튼 (숨김, JavaScript에서 호출)
    if st.button("", key=f"close-btn-{key}", help="닫기"):
        st.session_state[f"{key}_open"] = False
        st.rerun()
    
    # 모달 본문
    st.markdown(f'<div class="modal-body-{key}">', unsafe_allow_html=True)
    
    try:
        yield
    finally:
        # 모달 본문 닫기
        st.markdown('</div>', unsafe_allow_html=True)
        # 모달 컨테이너 닫기
        st.markdown('</div>', unsafe_allow_html=True)
        # 모달 오버레이 닫기
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 오버레이 클릭 시 닫기 JavaScript
        st.markdown(
            f"""
            <script>
            (function() {{
                const overlay = document.getElementById('modal-overlay-{key}');
                const closeBtn = document.querySelector('[data-testid="baseButton-secondary"][aria-label="닫기"]');
                
                if (overlay && closeBtn) {{
                    overlay.addEventListener('click', function(e) {{
                        if (e.target === overlay) {{
                            closeBtn.click();
                        }}
                    }});
                }}
            }})();
            </script>
            """,
            unsafe_allow_html=True
        )


def open_modal(key: str):
    """모달 열기"""
    st.session_state[f"{key}_open"] = True


def close_modal(key: str):
    """모달 닫기"""
    st.session_state[f"{key}_open"] = False
