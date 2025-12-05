"""회원가입 컴포넌트"""
import streamlit as st
from service import AuthService, ProfileService, StreakService, PointsService
from utils.auth import login_user, hash_password
import re


def validate_email(email: str) -> bool:
    """이메일 형식 검증"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """비밀번호 검증"""
    if len(password) < 6:
        return False, "비밀번호는 최소 6자 이상이어야 합니다."
    return True, ""


def render_signup_page():
    """회원가입 페이지 렌더링"""
    # 사이드바 숨기기
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none !important; }
        section[data-testid="stMain"] { margin-left: 0 !important; }
        button[data-testid="baseButton-header"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 중앙 정렬을 위한 컬럼 사용
    col1, col2, col3 = st.columns([1, 4, 1], gap="large")
    
    with col2:
        # 제목
        st.markdown("# 💪 체력 FIT")
        st.markdown("#### 회원가입")
        st.markdown("---")
        
        # 회원가입 폼
        with st.form("signup_form", clear_on_submit=False):
            # 이름 입력
            name = st.text_input(
                "이름 *",
                placeholder="이름을 입력하세요",
                key="signup_name"
            )
            
            # 이메일 입력
            email = st.text_input(
                "이메일 *",
                placeholder="example@email.com",
                key="signup_email"
            )
            
            # 비밀번호 입력
            password = st.text_input(
                "비밀번호 *",
                type="password",
                placeholder="최소 6자 이상",
                key="signup_password"
            )
            
            # 비밀번호 확인
            password_confirm = st.text_input(
                "비밀번호 확인 *",
                type="password",
                placeholder="비밀번호를 다시 입력하세요",
                key="signup_password_confirm"
            )
            
            # 생년월일
            birth_year = st.number_input(
                "출생년도 *",
                min_value=1950,
                max_value=2020,
                value=2000,
                step=1,
                key="signup_birth_year"
            )
            
            # 성별
            gender = st.radio(
                "성별 *",
                ["남성", "여성"],
                horizontal=True,
                key="signup_gender"
            )
            
            # 지역
            region = st.text_input(
                "지역",
                placeholder="예: 서울시-강남구",
                key="signup_region"
            )
            
            # 약관 동의
            st.markdown("---")
            terms_agreed = st.checkbox(
                "서비스 이용약관에 동의합니다 *",
                key="signup_terms"
            )
            
            # 제출 버튼
            submitted = st.form_submit_button(
                "회원가입",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                # 유효성 검사
                errors = []
                
                if not name or not name.strip():
                    errors.append("이름을 입력해주세요.")
                
                if not email or not email.strip():
                    errors.append("이메일을 입력해주세요.")
                elif not validate_email(email):
                    errors.append("올바른 이메일 형식을 입력해주세요.")
                
                if not password:
                    errors.append("비밀번호를 입력해주세요.")
                else:
                    is_valid, error_msg = validate_password(password)
                    if not is_valid:
                        errors.append(error_msg)
                
                if password != password_confirm:
                    errors.append("비밀번호가 일치하지 않습니다.")
                
                if not terms_agreed:
                    errors.append("서비스 이용약관에 동의해주세요.")
                
                # 에러가 있으면 표시
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # 회원가입 처리
                    auth_service = AuthService()
                    profile_service = ProfileService()
                    streak_service = StreakService()
                    points_service = PointsService()
                    
                    # 이메일 중복 체크
                    existing_user = auth_service.get_user_by_email(email)
                    if existing_user:
                        st.error("이미 사용 중인 이메일입니다.")
                    else:
                        # 사용자 ID 생성 (이메일 기반 또는 이름 기반)
                        user_id = f"user_{name.lower().replace(' ', '_')}"
                        
                        # ID 중복 체크 및 처리
                        counter = 1
                        original_user_id = user_id
                        while auth_service.get_user_by_id(user_id):
                            user_id = f"{original_user_id}_{counter}"
                            counter += 1
                        
                        # 나이 그룹 계산
                        from datetime import datetime
                        current_year = datetime.now().year
                        age = current_year - birth_year
                        if age < 20:
                            age_group = "10-19"
                        elif age < 25:
                            age_group = "20-24"
                        elif age < 30:
                            age_group = "25-29"
                        elif age < 35:
                            age_group = "30-34"
                        elif age < 40:
                            age_group = "35-39"
                        elif age < 45:
                            age_group = "40-44"
                        elif age < 50:
                            age_group = "45-49"
                        elif age < 55:
                            age_group = "50-54"
                        elif age < 60:
                            age_group = "55-59"
                        else:
                            age_group = "60+"
                        
                        # 사용자 생성 (auth_data.json과 profile_data.json에 모두 저장)
                        success = auth_service.create_user(
                            user_id=user_id,
                            name=name,
                            email=email,
                            password_hash=hash_password(password),
                            provider="local",
                            nickname=name,
                            gender="M" if gender == "남성" else "F",
                            birth_year=birth_year,
                            age_group=age_group,
                            region=region or "서울시-강남구",
                            avatar="👤"
                        )
                        
                        if success:
                            # 연속 측정 데이터 초기화
                            streak_service.initialize_streak(user_id)
                            # 포인트 데이터 초기화
                            points_service.initialize_user_points(user_id)
                            
                            # 토스트 알림 표시 (3초 후 자동 사라짐)
                            st.toast("✅ 회원가입이 완료되었습니다!", icon="🎉")
                            
                            # 로그인 페이지로 이동
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error("회원가입 중 오류가 발생했습니다.")
        
        # 로그인 페이지로 이동
        st.markdown("---")
        st.markdown("이미 계정이 있으신가요?")
        if st.button("로그인하기", use_container_width=True, key="go_to_login"):
            st.session_state.page = "login"
            st.rerun()


def render(go_to=None):
    """회원가입 페이지 렌더링 (routes.py 호환)"""
    render_signup_page()

