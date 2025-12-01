import streamlit as st
import json

def render(go_to):
    st.title("📹 푸시업 분석 (브라우저 기반)")

    # 유저 업로드
    video_file = st.file_uploader("분석할 영상을 업로드하세요", type=["mp4", "mov"])

    if not video_file:
        return

    # 영상 base64 인코딩
    import base64
    video_bytes = video_file.read()
    video_b64 = base64.b64encode(video_bytes).decode()

    st.markdown("### 🔍 브라우저에서 푸시업을 분석 중입니다...")

    # JS 삽입
    st.components.v1.html(f"""
    <html>
    <body>

    <video id="inputVideo" controls style="width: 100%;"></video>
    <script>
        const video = document.getElementById('inputVideo');
        video.src = "data:video/mp4;base64,{video_b64}";

        // MediaPipe JS (Pose)
        import("https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.4/pose.js")
        .then(() => {
            const pose = new Pose.Pose({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.4/${file}`
            });

            pose.setOptions({
                modelComplexity: 1,
                smoothLandmarks: true,
                enableSegmentation: false,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });

            // 분석 결과 저장
            let results_list = [];

            pose.onResults((results) => {
                if (results.poseLandmarks) {
                    results_list.push(results.poseLandmarks);
                }
            });

            // 영상 프레임 처리
            const camera = new Camera(video, {
                onFrame: async () => {
                    await pose.send({image: video});
                }
            });
            camera.start();

            // 분석 완료 → Python으로 전달
            video.onended = () => {
                const streamlitMsg = JSON.stringify({landmarks: results_list});
                const pyChannel = window.parent;
                pyChannel.postMessage(streamlitMsg, "*");
            };
        });
    </script>

    </body>
    </html>
    """, height=600)

    # JS → Python 메시지 listener
    js_msg = st.experimental_get_query_params().get("js_msg")

    if js_msg:
        data = json.loads(js_msg[0])
        st.write("📌 **JS에서 전달한 keypoints**")
        st.json(data)
