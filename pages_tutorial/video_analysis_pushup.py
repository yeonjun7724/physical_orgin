# pages/video_analysis_pushup.py
import streamlit as st
import cv2
import tempfile

from modules.pose_yolo import YoloPoseDetector
from modules.pushup_analyzer_yolo import PushupAnalyzerYolo

def render(go_to):
    st.title("📊 팔굽혀펴기 영상 분석 결과")

    uploaded_file = st.session_state.get("uploaded_video", None)

    if uploaded_file is None:
        st.error("먼저 팔굽혀펴기 튜토리얼에서 영상을 업로드해주세요.")
        if st.button("튜토리얼로 이동"):
            go_to("tutorial_pushup")
        return

    # 사용자 정보 (없으면 기본값)
    user_age = st.session_state.get("user_age", 25)
    user_gender = st.session_state.get("user_gender", "남")

    # 임시 파일로 저장
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.flush()

    cap = cv2.VideoCapture(tfile.name)

    if not cap.isOpened():
        st.error("영상을 열 수 없습니다.")
        return

    detector = YoloPoseDetector()
    analyzer = PushupAnalyzerYolo()

    st.write("⏳ 영상을 분석 중입니다... (영상 길이에 따라 다소 시간이 걸릴 수 있습니다)")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # 안전장치

    # 분석 부하 줄이기: 초당 5프레임만 분석
    frame_interval = max(1, int(fps // 5))
    frame_idx = 0
    processed_frames = 0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    progress = st.progress(0.0)
    status_text = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            keypoints = detector.detect_keypoints(frame)
            analyzer.process_frame(keypoints)
            processed_frames += 1

        frame_idx += 1

        # 진행률 업데이트
        if total_frames > 0:
            progress_ratio = min(1.0, frame_idx / total_frames)
            progress.progress(progress_ratio)
            status_text.text(f"분석 중... ({frame_idx}/{total_frames} 프레임)")

    cap.release()

    progress.progress(1.0)
    status_text.text("분석 완료!")

    # 결과 요약
    count = analyzer.pushup_count
    quality = analyzer.avg_quality_score()
    grade = analyzer.calculate_kspo_grade(count, user_age, user_gender)

    st.subheader("📌 팔굽혀펴기 자동 분석 결과")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("횟수", f"{count} 회")
    with col2:
        st.metric("자세 품질 점수", f"{quality} / 100")
    with col3:
        st.metric("예상 등급 (국민체력100 기반)", grade)

    st.markdown("---")
    st.write(f"- 분석 대상: {user_age}세 / {user_gender}")
    st.write("- 등급 기준은 국민체력100 근지구력(팔굽혀펴기) 표를 단순화한 예시이며, 실제 공식 평가와는 차이가 있을 수 있습니다.")

    if st.button("팔굽혀펴기 튜토리얼로 돌아가기"):
        go_to("tutorial_pushup")
