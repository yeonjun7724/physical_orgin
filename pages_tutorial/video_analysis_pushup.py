import streamlit as st
import base64
import json

def render(go_to):
    st.title("📹 푸시업 분석 (브라우저 기반)")

    video_file = st.file_uploader("분석할 영상을 업로드하세요", type=["mp4", "mov"])
    if not video_file:
        return

    # Base64 변환
    video_bytes = video_file.read()
    video_b64 = base64.b64encode(video_bytes).decode()

    st.markdown("### 🔍 브라우저에서 영상 분석 중...")

    # f-string 제거 → .format() 사용
    html_code = """
    <html>
    <body>

    <video id="inputVideo" controls style="width:100%;"></video>

    <script type="module">
        const videoTag = document.getElementById("inputVideo");
        videoTag.src = "data:video/mp4;base64,{video_b64}";

        import * as mpPose from "https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.4/pose.js";
        import * as cam from "https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js";

        let pose = new mpPose.Pose({
            locateFile: (file) => "https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.4/" + file
        });

        pose.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            enableSegmentation: false,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        let resultsList = [];

        pose.onResults((results) => {
            if (results.poseLandmarks) {
                resultsList.push(results.poseLandmarks);
            }
        });

        const camera = new cam.Camera(videoTag, {
            onFrame: async () => {
                await pose.send({ image: videoTag });
            }
        });

        camera.start();

        videoTag.onended = () => {
            const msg = JSON.stringify({ landmarks: resultsList });
            window.parent.postMessage(msg, "*");
        };
    </script>

    </body>
    </html>
    """.format(video_b64=video_b64)

    st.components.v1.html(html_code, height=700)

    js_msg = st.experimental_get_query_params().get("js_msg")
    if js_msg:
        data = json.loads(js_msg[0])
        st.write("📌 분석 결과 (keypoints)")
        st.json(data)
