import streamlit as st
import time
import requests
import os
import numpy as np
import cv2

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FARMIO", layout="wide")

API_KEY = "215a66be-fcc4-11f0-a6b2-0200cd936042"
TEMPLATE = "FARMIO_OTP"

# ---------------- FIELD DETECTION (TEMP DEMO LOGIC) ----------------
def looks_like_field(frames):
    if not frames:
        return False

    green_pixels = 0
    total_pixels = 0

    for img in frames[:10]:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        green_pixels += np.sum(mask > 0)
        total_pixels += mask.size

    return (green_pixels / total_pixels) > 0.20


# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "language" not in st.session_state:
    st.session_state.language = "English"

if "farmer_verified" not in st.session_state:
    st.session_state.farmer_verified = False
if "face_live_verified" not in st.session_state:
    st.session_state.face_live_verified = False
if "field_verified" not in st.session_state:
    st.session_state.field_verified = False
if "field_type" not in st.session_state:
    st.session_state.field_type = None
if "field_video_path" not in st.session_state:
    st.session_state.field_video_path = None

# ---------------- SPLASH ----------------
if st.session_state.page == "splash":
    st.markdown("## 🌾 FARMIO")
    time.sleep(1)
    st.session_state.page = "farmer"
    st.rerun()

# ---------------- FARMER ----------------
elif st.session_state.page == "farmer":
    st.header("Farmer Login")
    if st.button("Continue"):
        st.session_state.page = "farmer_video"
        st.rerun()

# ---------------- FARMER VIDEO ----------------
elif st.session_state.page == "farmer_video":
    st.header("🌾 Farmer Live Verification")

    try:
        from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase

        class Recorder(VideoProcessorBase):
            def __init__(self):
                self.frames = []
                self.recording = False

            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")
                if self.recording:
                    self.frames.append(img)
                return frame

            def start(self):
                self.frames = []
                self.recording = True

            def stop(self):
                self.recording = False

        # -------- FACE --------
        st.subheader("Step 1: FACE (Live Required)")
        ctx_face = webrtc_streamer(
            key="face",
            mode=WebRtcMode.SENDONLY,
            video_processor_factory=Recorder,
            media_stream_constraints={"video": True, "audio": False},
        )

        if st.button("Complete FACE Verification"):
            if ctx_face and ctx_face.video_processor:
                vp = ctx_face.video_processor
                vp.start()
                time.sleep(2)
                vp.stop()

                if len(vp.frames) >= 10:
                    st.session_state.face_live_verified = True
                    st.success("✅ Face verified")
                else:
                    st.error("❌ Face not verified")

        # -------- FIELD --------
        if st.session_state.face_live_verified:
            st.subheader("Step 2: FIELD (Live or Demo)")

            ctx_field = webrtc_streamer(
                key="field",
                mode=WebRtcMode.SENDONLY,
                video_processor_factory=Recorder,
                media_stream_constraints={"video": True, "audio": False},
            )

            if st.button("Complete FIELD Live"):
                if ctx_field and ctx_field.video_processor:
                    vp = ctx_field.video_processor
                    vp.start()
                    st.info("📹 Recording field…")
                    time.sleep(3)
                    vp.stop()

                    if len(vp.frames) >= 15 and looks_like_field(vp.frames):
                        os.makedirs("uploads", exist_ok=True)
                        h, w, _ = vp.frames[0].shape
                        path = f"uploads/field_live_{int(time.time())}.mp4"

                        out = cv2.VideoWriter(
                            path,
                            cv2.VideoWriter_fourcc(*"mp4v"),
                            20,
                            (w, h)
                        )
                        for f in vp.frames:
                            out.write(f)
                        out.release()

                        st.session_state.field_verified = True
                        st.session_state.field_type = "live"
                        st.session_state.field_video_path = path
                        st.success("✅ Field verified (LIVE)")

                    else:
                        st.session_state.field_verified = False
                        st.warning("⚠️ This does not look like a field. Please upload demo video.")

            # -------- DEMO --------
            if not st.session_state.field_verified:
                demo = st.file_uploader("Upload FIELD Demo Video", type=["mp4"])
                if demo:
                    os.makedirs("uploads", exist_ok=True)
                    demo_path = f"uploads/field_demo_{int(time.time())}.mp4"
                    with open(demo_path, "wb") as f:
                        f.write(demo.getbuffer())

                    st.session_state.field_verified = True
                    st.session_state.field_type = "demo"
                    st.session_state.field_video_path = demo_path
                    st.success("✅ Demo FIELD uploaded")

        # -------- FINAL GATE --------
        if st.session_state.face_live_verified and st.session_state.field_verified:
            st.session_state.farmer_verified = True
            st.session_state.page = "consumer"
            st.rerun()

    except Exception as e:
        st.error("Live camera not supported")

# ---------------- CONSUMER ----------------
elif st.session_state.page == "consumer":
    st.header("🛒 Consumer Dashboard")

    if st.session_state.field_video_path and os.path.exists(st.session_state.field_video_path):
        st.video(st.session_state.field_video_path)
    else:
        st.warning("⚠️ Field not verified yet")
