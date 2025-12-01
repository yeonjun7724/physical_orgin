import streamlit as st
import tempfile
import cv2
from modules.pose_yolo import YoloPoseDetector
from modules.pushup_analyzer_yolo import PushupAnalyzerYolo

def safe_age_to_int(value):
    """
    숫자 또는 '20-24' 같은 구간 문자열을 안전하게 정수로 변환.
    """
    try:
        return int(value)  # 원래 숫자면 그대로 변환
    except:
        pass

    try:
        # '20-24' 형태면 중앙값 계산
        if isinstance(value, str) and "-" in value:
            a, b = value.split("-")
            return (int(a) + int(b)) // 2
    except:
        pass

    # 변환 실패하면 기본값 반환
    return 25


def render(go_to=None, **kwargs):

    st.title("📊 푸시업 분석 (브라우저 기반)")

    uploaded_file = st.file_uploader(
        "업로드할 푸시업 영상을 선택하세요",
        type=["mp4", "mov", "m4v"],
        key="pushup_video_uploader"
    )

    if uploaded_file is None:
        st.info("푸시업 영상을 업로드하면 분석이 시작됩니다.")
        return

    # 파일명 안전 처리
    safe_filename = uploaded_file.name.replace("\n", "_").replace("\r", "_")

    # 🎯 나이를 안전하게 숫자로 변환
    user_age_raw = st.session_state.get("user_age", 25)
    user_age = safe_age_to_int(user_age_raw)

    user_gender = st.session_state.get("user_gender", "남")

    # 임시 파일 생성
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=safe_filename)
    tfile.write(uploaded_file.read())
    tfile.flush()

    # 모델 초기화
    detector = YoloPoseDetector()
    analyzer = PushupAnalyzerYolo()

    st.write("⏳ *브라우저에서 영상 분석 중…*")
    progress = st.empty()

    cap = cv2.VideoCapture(tfile.name)

    if not cap.isOpened():
        st.error("⚠ 영상을 열 수 없습니다.")
        return

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        idx += 1
        progress.progress(idx / max(total, 1))

        keypoints = detector.detect_keypoints(frame)
        analyzer.process_frame(keypoints)

    cap.release()

    # 결과 계산
    count = int(analyzer.pushup_count)
    quality = float(analyzer.avg_quality_score())

    grade = analyzer.calculate_kspo_grade(
        pushup_count=count,
        age=user_age,
        gender=user_gender
    )

    # 출력
    st.subheader("📌 분석 결과")
    c1, c2, c3 = st.columns(3)
    c1.metric("횟수", f"{count}회")
    c2.metric("자세 점수", f"{quality:.1f}/100")
    c3.metric("예상 등급", grade)

    st.markdown("---")
    st.write(f"👤 나이: {user_age_raw} (→ 변환값 {user_age}) / 성별: {user_gender}")
    st.write("※ 국민체력100 기준을 단순화하여 적용한 참고용 결과입니다.")
