import streamlit as st
import cv2
import tempfile
from modules.pose_detector import PoseDetector
from modules.pushup_analyzer import PushupAnalyzer

def render(go_to):
    st.title("📊 영상 분석 결과")

    uploaded_file = st.session_state.get("uploaded_video", None)

    if uploaded_file is None:
        st.error("먼저 튜토리얼에서 영상을 업로드해주세요.")
        return

    # 임시 파일로 저장
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # OpenCV로 파일 로드
    cap = cv2.VideoCapture(tfile.name)

    detector = PoseDetector()
    analyzer = PushupAnalyzer()

    st.write("⏳ 영상을 분석 중입니다...")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps // 5)  # 분석 부하 줄이기 위해 1초에 5프레임만 사용

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            landmarks = detector.detect(frame)
            analyzer.process_frame(landmarks)

        frame_idx += 1

    cap.release()

    # 분석 결과
    count = analyzer.pushup_count
    quality = analyzer.avg_quality_score()

    st.subheader("📌 팔굽혀펴기 분석 결과")
    st.metric("총 횟수", f"{count} 회", delta=None)
    st.metric("자세 정확도 점수", f"{quality} 점")

    # 국민체력100 등급 계산
    grade = analyzer.calculate_kspo_grade(count, st.session_state.get("user_age", 25), st.session_state.get("user_gender", "남"))
    st.metric("예상 등급(KSPO)", grade)

    if st.button("돌아가기"):
        go_to("tutorial_pushup")
