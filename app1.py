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

# ---------------- LANGUAGE DATA ----------------
languages = {
    "English": {"welcome": "Welcome to FARMIO", "farmer": "Farmer", "consumer": "Consumer"},
    "Tamil": {"welcome": "FARMIO-க்கு வரவேற்கிறோம்", "farmer": "விவசாயி", "consumer": "நுகர்வோர்"},
    "Malayalam": {"welcome": "FARMIOയിലേക്ക് സ്വാഗതം", "farmer": "കർഷകൻ", "consumer": "ഉപഭോക്താവ്"},
    "Telugu": {"welcome": "FARMIO కి స్వాగతం", "farmer": "రైతు", "consumer": "వినియోగదారు"},
    "Marathi": {"welcome": "FARMIO मध्ये आपले स्वागत आहे", "farmer": "शेतकरी", "consumer": "ग्राहक"},
    "Kannada": {"welcome": "FARMIO ಗೆ ಸ್ವಾಗತ", "farmer": "ರೈತ", "consumer": "ಗ್ರಾಹಕ"},
    "Bengali": {"welcome": "FARMIO তে আপনাকে স্বাগতম", "farmer": "কৃষক", "consumer": "ভোক্তা"},
    "Gujarati": {"welcome": "FARMIO માં આપનું સ્વાગત છે", "farmer": "કિસાન", "consumer": "ગ્રાહક"},
    "Assamese": {"welcome": "FARMIO ত আপোনাক স্বাগতম", "farmer": "কৃষক", "consumer": "গ্ৰাহক"},
    "Odia": {"welcome": "FARMIOରେ ଆପଣଙ୍କୁ ସ୍ବାଗତ", "farmer": "କୃଷକ", "consumer": "ଗ୍ରାହକ"},
    "Bhojpuri": {"welcome": "FARMIO में राउर स्वागत बा", "farmer": "किसान", "consumer": "ग्राहक"},
    "Hindi": {"welcome": "FARMIO में आपका स्वागत है", "farmer": "किसान", "consumer": "उपभोक्ता"},
    "Punjabi": {"welcome": "FARMIO ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ", "farmer": "ਕਿਸਾਨ", "consumer": "ਗ੍ਰਾਹਕ"},
    "Urdu": {"welcome": "FARMIO میں خوش آمدید", "farmer": "کسان", "consumer": "صارف"},
}

native_names = {
    "English": "English",
    "Tamil": "தமிழ்",
    "Malayalam": "മലയാളം",
    "Telugu": "తెలుగు",
    "Marathi": "मराठी",
    "Kannada": "ಕನ್ನಡ",
    "Bengali": "বাংলা",
    "Gujarati": "ગુજરાતી",
    "Assamese": "অসমীয়া",
    "Odia": "ଓଡ଼ିଆ",
    "Bhojpuri": "भोजपुरी",
    "Hindi": "हिन्दी",
    "Punjabi": "ਪੰਜਾਬੀ",
    "Urdu": "اردو",
}

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
if "consumer_logged_in" not in st.session_state:
    st.session_state.consumer_logged_in = False
if "consumer_verified" not in st.session_state:
    st.session_state.consumer_verified = False
if "show_welcome_page" not in st.session_state:
    st.session_state.show_welcome_page = False
# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #f0fff0; }
div.stButton > button {
    background-color: #2f7d32;
    color: white;
    height: 50px;
    width: 200px;
    border-radius: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SPLASH SCREEN ----------------
if st.session_state.page == "splash":

    logo_path = os.path.join(os.path.dirname(__file__), "A_logo_for_WEXPO_2026.png")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(logo_path):
            st.image(logo_path, width=180)
        else:
            st.error("Logo not found")

    st.markdown("""
    <div style="text-align:center; background:#e6ffe6; padding:15px; border-radius:15px;">
        <h1 style="color:#2f7d32;">FARMIO</h1>
        <p style="color:#2f7d32;">Connecting Farmers & Consumers</p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)
    st.session_state.page = "language"
    st.rerun()

# ---------------- LANGUAGE ----------------
elif st.session_state.page == "language":
    st.header("Select Language")
    cols = st.columns(3)
    for i, lang in enumerate(native_names):
        if cols[i % 3].button(native_names[lang]):
            st.session_state.language = lang
            st.session_state.page = "user_type"
            st.rerun()

# ---------------- USER TYPE ----------------
elif st.session_state.page == "user_type":
    text = languages[st.session_state.language]
    c1, c2 = st.columns(2)
    if c1.button(f"👨‍🌾 {text['farmer']}"):
        st.session_state.page = "farmer"
        st.rerun()
    if c2.button(f"🛒 {text['consumer']}"):
        st.session_state.page = "consumer_login"
        st.rerun()


# ---------------- FARMER LOGIN ----------------
elif st.session_state.page == "farmer":
    st.header("Farmer Login (OTP)")
    phone = st.text_input("Mobile Number")

    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.session_id = res["Details"]
                st.success("OTP sent")
        else:
            st.error("Invalid number")

    if "session_id" in st.session_state:
        otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.session_id}/{otp}"
            result = requests.get(verify_url).json()
            if result["Status"] == "Success":
                st.session_state.page = "farmer_video"
                st.rerun()

# ---------------- FARMER VIDEO (LIVE) ----------------
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
        
# ---------------- FARMER DASHBOARD ----------------
elif st.session_state.page == "farmer_dashboard":

    st.markdown("<h2 style='color:#2f7d32'>Farmer Dashboard</h2>", unsafe_allow_html=True)

    if st.session_state.farmer_verified:
        st.success("Verified Farmer ")

    if st.button("Sell Product"):
        st.session_state.page = "product_upload"
        st.rerun()

# ---------------- CONSUMER LOGIN ----------------
elif st.session_state.page == "consumer_login":
    st.header("Consumer Login (OTP)")
    phone = st.text_input("Mobile Number (10 digits)")
    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.consumer_session_id = res["Details"]
                st.success("OTP sent 📲")
    if "consumer_session_id" in st.session_state and not st.session_state.consumer_verified:
        otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.consumer_session_id}/{otp}"
            verify_res = requests.get(verify_url).json()
            if verify_res["Status"] == "Success":
                st.session_state.consumer_verified = True
                st.session_state.consumer_logged_in = True
                st.session_state.show_welcome_page = True 
                st.session_state.page = "consumer_dashboard"
                st.rerun()
# ---------------- CONSUMER WELCOME PAGE ----------------
if st.session_state.page == "consumer_welcome":
    st.markdown(f"<h2 style='color:#2f7d32;'>Welcome to FARMIO!</h2>", unsafe_allow_html=True)
    st.write("You are now logged in as a consumer.")
    
    if st.button("Continue to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- CONSUMER PAGES ----------------
elif st.session_state.consumer_logged_in:
    st.sidebar.title("FARMIO")
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "History", "Farmer Proof", "Compare", "Profile"]
    )
    st.session_state.page = menu.lower()

    if st.session_state.page == "dashboard":
        st.title("Verify Before You Buy")
        col1, col2 = st.columns([3,1])
        with col1:
            market = st.selectbox("Market Area", ["Local Market", "City Market"])
        with col2:
            st.write("👤 Customer")
        uploaded = st.file_uploader("Upload product image", type=["jpg","png","jpeg"])
        if uploaded:
            st.image(uploaded, width=250)
            st.metric("Quality Score", "72 / 100", "Medium")
            st.table({
                "Source": ["Marketplace", "Fair Price", "Verified Farmers"],
                "Price": ["₹90/kg", "₹55–₹65/kg", "₹54–₹58/kg"],
                "Status": ["Overpriced", "Fair", "Fair"]
            })

    elif st.session_state.page == "history":
        st.title("Verification History")
        st.info("All previously verified products will appear here.")

    elif st.session_state.page == "farmer proof":
        st.title("Verified Farmer Quality Library")
        st.success("Showing verified harvest proofs")

    elif st.session_state.page == "compare":
        st.title("Product Comparison")
        st.write("Marketplace vs Verified Farmer")

    elif st.session_state.page == "profile":
        st.title("Profile & Settings")
        st.write("👤 **Consumer Profile**")
        st.write("- Name: N/A")
        st.write("- Mobile Number: (Hidden)")
        st.write("- Status: Verified Consumer ✅")
        if st.button("Logout"):
            st.session_state.consumer_logged_in = False
            st.session_state.consumer_verified = False
            st.session_state.page = "consumer_login"
            st.experimental_rerun()


    
   








