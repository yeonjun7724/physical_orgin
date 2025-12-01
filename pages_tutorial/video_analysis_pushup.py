import streamlit as st
import tempfile
from modules.pose_yolo import YoloPoseDetector
from modules.pushup_analyzer_yolo import PushupAnalyzerYolo

def render(go_to):
    st.title("📊 푸시업 분석 (브라우저 기반)")

    uploaded_file = st.file_uploader("업로드할 푸시업 영상을 선택하세요", type=["mp4", "mov", "m4v"])

    if uploaded_file is None:
        st.info("푸시업 영상을 업로드하면 분석이 시작됩니다.")
        return

    # 사용자 정보
    user_age = st.session_state.get("user_age", 25)
    user_gender = st.session_state.get("user_gender", "남")

    # 브라우저에서 바로 데이터를 읽기 위해 파일로 저장
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    tfile.flush()

    # YOLO pose detector & 분석기
    detector = YoloPoseDetector()
    analyzer = PushupAnalyzerYolo()

    st.write("⏳ *브라우저에서 영상 분석 중…*")
    progress = st.empty()

    import cv2
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
        progress.progress(idx / total)

        keypoints = detector.detect_keypoints(frame)
        analyzer.process_frame(keypoints)

    cap.release()

    # 최종 결과
    count = analyzer.pushup_count
    quality = analyzer.avg_quality_score()
    grade = analyzer.calculate_kspo_grade(count, user_age, user_gender)

    st.subheader("📌 분석 결과")
    c1, c2, c3 = st.columns(3)
    c1.metric("횟수", f"{count}회")
    c2.metric("자세 점수", f"{quality}/100")
    c3.metric("예상 등급", grade)

    st.markdown("---")
    st.write(f"👤 나이: {user_age}세 / 성별: {user_gender}")
    st.write("※ 국민체력100 기준을 단순화하여 적용한 참고용 결과입니다.")
