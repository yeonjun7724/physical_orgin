import streamlit as st
import importlib.util
import os

# other_pages 는 숫자 접두사를 사용하지 않는다고 가정
try:
   from other_pages import (
      measure, result, signup,
      tutorial_pushup, tutorial_situp, tutorial_squat,
      tutorial_balance, tutorial_knee_lift, tutorial_trunk_flex
   )
except Exception as e:
   import streamlit as st
   st.warning(f"other_pages 모듈 import 오류: {str(e)}")
   measure = result = signup = None
   tutorial_pushup = tutorial_situp = tutorial_squat = None
   tutorial_balance = tutorial_knee_lift = tutorial_trunk_flex = None

def go_to(page_name): # 페이지 이동
   st.session_state.page = page_name
   st.rerun()

def _pages_dir() -> str:
   return os.path.join(os.path.dirname(os.path.dirname(__file__)), "pages")


# pages 디렉토리 내 숫자 접두사 파일 매핑 (사이드바에 표시되는 페이지들)
PAGE_FILE_MAP = {
   "home": "01_home.py",
   "select_exercise": "02_select_exercise.py",
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
      return None
   spec = importlib.util.spec_from_file_location(f"pages__{page_name}", file_path)
   if spec is None or spec.loader is None:
      return None
   module = importlib.util.module_from_spec(spec)
   # 모듈 로드 시 sys.path에 현재 디렉토리 추가 (import 경로 문제 해결)
   import sys
   current_dir = os.path.dirname(os.path.dirname(__file__))
   if current_dir not in sys.path:
      sys.path.insert(0, current_dir)
   try:
      spec.loader.exec_module(module)
      return module
   except Exception as e:
      st.error(f"페이지 로드 오류 ({page_name}): {str(e)}")
      return None


def _call_render(module, go_to_cb):
   if module is None:
      st.warning("페이지 모듈을 로드할 수 없습니다.")
      return
   render_func = getattr(module, "render", None)
   if render_func is None:
      st.warning("페이지에 render 함수가 없습니다.")
      return
   # app.py에서 렌더링 중임을 표시 (각 페이지 파일의 자동 실행 방지)
   st.session_state._rendered_by_app = True
   try:
      # 먼저 go_to 를 넘겨 호출 시도
      render_func(go_to_cb)
   except TypeError:
      # 시그니처가 다르면 인자 없이 호출
      try:
         render_func()
      except Exception as e:
         st.error(f"페이지 렌더링 오류: {str(e)}")
         import traceback
         st.code(traceback.format_exc())
   except Exception as e:
      st.error(f"페이지 렌더링 오류: {str(e)}")
      import traceback
      st.code(traceback.format_exc())
   finally:
      # 렌더링 완료 후 플래그 유지 (다음 실행에서 중복 방지)
      pass


def _render_other_page(page_name: str, go_to_cb):
    """other_pages 렌더링 헬퍼 함수 (사이드바에 표시되지 않는 페이지들)"""
    page_map = {
        "measure": measure,
        "result": result,
        "signup": signup,
        "tutorial_pushup": tutorial_pushup,
        "tutorial_situp": tutorial_situp,
        "tutorial_squat": tutorial_squat,
        "tutorial_balance": tutorial_balance,
        "tutorial_knee_lift": tutorial_knee_lift,
        "tutorial_trunk_flex": tutorial_trunk_flex,
    }
    page_module = page_map.get(page_name)
    if page_module is None:
        st.error(f"페이지 모듈을 찾을 수 없습니다: {page_name}")
        st.info(f"사용 가능한 other_pages: measure, result, signup, tutorial_pushup, tutorial_situp, tutorial_squat, tutorial_balance, tutorial_knee_lift, tutorial_trunk_flex")
        st.info(f"사이드바 페이지: {', '.join(PAGE_FILE_MAP.keys())}")
        return
    _call_render(page_module, go_to_cb)


def sidebar_page(page_name): # 사이드바 페이지 렌더링
   current = st.session_state.page
   if current in PAGE_FILE_MAP:
      module = _load_page_module(current)
      _call_render(module, go_to)
   else:
      _render_other_page(current, go_to)

def render_page(page_name: str | None = None): # 페이지 라우팅
   target = page_name or st.session_state.get("page", "home")
   if target in PAGE_FILE_MAP:
      module = _load_page_module(target)
      _call_render(module, go_to)
   else:
      _render_other_page(target, go_to)