import streamlit as st
import importlib.util
import os
import sys


# ============================
# 💡 1) 프로젝트 루트 및 페이지 폴더 경로 설정
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))        # project_root/utils → project_root
PAGES_TUTORIAL_DIR = os.path.join(BASE_DIR, "pages_tutorial")
OTHER_PAGES_DIR = os.path.join(BASE_DIR, "other_pages")
PAGES_AUTH_DIR = os.path.join(BASE_DIR, "pages_auth")

# sys.path에 없으면 추가
for path in [BASE_DIR, PAGES_TUTORIAL_DIR, OTHER_PAGES_DIR, PAGES_AUTH_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)



# ============================
# 💡 2) lazy import 대상 변수 선언
# ============================

measure = result = signup = login = None

tutorial_pushup = tutorial_situp = tutorial_squat = None
tutorial_balance = tutorial_knee_lift = tutorial_trunk_flex = None

video_analysis_pushup = None    # ⭐ 분석 페이지




# ============================
# 💡 3) lazy import
# ============================

def _import_other_pages():
    global measure, result, signup, login
    global tutorial_pushup, tutorial_situp, tutorial_squat
    global tutorial_balance, tutorial_knee_lift, tutorial_trunk_flex
    global video_analysis_pushup

    if measure is not None:
        return

    try:
        # 기본 페이지
        import other_pages.measure as measure_mod
        import other_pages.result as result_mod

        # Auth
        import pages_auth.signup as signup_mod
        import pages_auth.login as login_mod

        # 튜토리얼 (modules 폴더)
        import pages_tutorial.tutorial_pushup as tutorial_pushup_mod
        import pages_tutorial.tutorial_situp as tutorial_situp_mod
        import pages_tutorial.tutorial_squat as tutorial_squat_mod
        import pages_tutorial.tutorial_balance as tutorial_balance_mod
        import pages_tutorial.tutorial_knee_lift as tutorial_knee_lift_mod
        import pages_tutorial.tutorial_trunk_flex as tutorial_trunk_flex_mod
        import pages_tutorial.video_analysis_pushup as video_analysis_pushup_mod

        # ⭐ 분석 페이지
        import pages_tutorial.modules.video_analysis_pushup as video_analysis_pushup_mod

        # 주입
        measure = measure_mod
        result = result_mod
        signup = signup_mod
        login = login_mod

        tutorial_pushup = tutorial_pushup_mod
        tutorial_situp = tutorial_situp_mod
        tutorial_squat = tutorial_squat_mod
        tutorial_balance = tutorial_balance_mod
        tutorial_knee_lift = tutorial_knee_lift_mod
        tutorial_trunk_flex = tutorial_trunk_flex_mod

        video_analysis_pushup = video_analysis_pushup_mod

    except Exception as e:
        st.warning(f"other_pages import 오류: {str(e)}")


# ============================
# 💡 4) 페이지 이동 기능
# ============================

def go_to(page_name: str):
    st.session_state.page = page_name
    st.rerun()



# ============================
# 💡 5) /pages 폴더에서 페이지 로딩
# ============================

def _pages_dir() -> str:
    return os.path.join(BASE_DIR, "pages")


PAGE_FILE_MAP = {
    "introduction": "01_introduction.py",
    "home": "02_home.py",
    "ranking": "03_ranking.py",
    "profile": "04_profile.py",
    "store": "05_store.py",
    "setting": "06_setting.py",
}




def _load_page_module(page_name: str):
    filename = PAGE_FILE_MAP.get(page_name)
    if not filename:
        return None

    file_path = os.path.join(_pages_dir(), filename)
    if not os.path.exists(file_path):
        st.error(f"페이지 파일이 없습니다: {file_path}")
        return None

    spec = importlib.util.spec_from_file_location(f"pages__{page_name}", file_path)
    if spec is None or spec.loader is None:
        st.error(f"{page_name} 모듈 로딩 실패")
        return None

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"페이지 로드 오류 ({page_name}): {str(e)}")
        return None




# ============================
# 💡 6) render() 호출
# ============================

def _call_render(module, go_to_cb):
    if module is None:
        st.warning("페이지 모듈을 로드할 수 없습니다.")
        return

    render_func = getattr(module, "render", None)
    if render_func is None:
        st.warning("render() 함수가 없는 페이지입니다.")
        return

    st.session_state._rendered_by_app = True

    try:
        render_func(go_to_cb)
    except TypeError:
        render_func()
    except Exception as e:
        st.error(f"페이지 렌더링 오류: {str(e)}")




# ============================
# 💡 7) other_pages / tutorial_pages / analysis_pages 렌더링
# ============================

def _render_other_page(page_name: str, go_to_cb):
    _import_other_pages()

    page_map = {
        # 기본
        "measure": measure,
        "result": result,
        "signup": signup,
        "login": login,

        # 튜토리얼
        "tutorial_pushup": tutorial_pushup,
        "tutorial_situp": tutorial_situp,
        "tutorial_squat": tutorial_squat,
        "tutorial_balance": tutorial_balance,
        "tutorial_knee_lift": tutorial_knee_lift,
        "tutorial_trunk_flex": tutorial_trunk_flex,

        # ⭐ 분석 페이지
        "video_analysis_pushup": video_analysis_pushup,
    }

    module = page_map.get(page_name)
    if module is None:
        st.error(f"잘못된 other_pages 요청: {page_name}")
        return

    _call_render(module, go_to_cb)




# ============================
# 💡 8) public API
# ============================

def render_page(page_name: str | None = None):
    target = page_name or st.session_state.get("page", "home")

    # 1) pages 폴더
    if target in PAGE_FILE_MAP:
        module = _load_page_module(target)
        _call_render(module, go_to)
    else:
        # 2) other_pages / pages_tutorial / analysis
        _render_other_page(target, go_to)



