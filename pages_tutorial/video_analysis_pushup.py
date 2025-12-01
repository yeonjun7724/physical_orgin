import streamlit as st
import tempfile
import cv2
from modules.pose_yolo import YoloPoseDetector
from modules.pushup_analyzer_yolo import PushupAnalyzerYolo

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

    # 파일 이름 안전 처리
    safe_filename = uploaded_file.name.replace("\n", "_").replace("\r", "_")

    # 사용자 정보 — 반드시 정수로 변환
    user_age = int(st.session_state.get("user_age", 25))
    user_gender = st.session_state.get("user_gender", "남")

    # 임시 파일 저장
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
        st.error("⚠ 영상을 열 수 없습니다. 업로드를 다시 시도해주세요.")
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

    # ----------- 🔥 타입 강제 변환 (가장 중요) ------------
    count = int(analyzer.pushup_count)
    quality = float(analyzer.avg_quality_score())
    # -------------------------------------------------------

    # 등급 계산
    grade = analyzer.calculate_kspo_grade(
        pushup_count=count,
        age=user_age,
        gender=user_gender
    )

    # 결과 출력
    st.subheader("📌 분석 결과")
    c1, c2, c3 = st.columns(3)
    c1.metric("횟수", f"{count}회")
    c2.metric("자세 점수", f"{quality:.1f}/100")
    c3.metric("예상 등급", grade)

    st.markdown("---")
    st.write(f"👤 나이: {user_age}세 / 성별: {user_gender}")
    st.write("※ 국민체력100 기준을 단순화하여 적용한 참고용 결과입니다.")
