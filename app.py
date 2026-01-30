import streamlit as st
import time
import requests
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FARMIO", layout="wide")

API_KEY = "215a66be-fcc4-11f0-a6b2-0200cd936042"
TEMPLATE = "FARMIO_OTP"

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

    st.markdown("<h2 style='text-align:center;color:#2f7d32'>Select Language</h2>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, lang in enumerate(native_names):
        if cols[i % 3].button(native_names[lang]):
            st.session_state.language = lang
            st.session_state.page = "user_type"
            st.rerun()

# ---------------- USER TYPE ----------------
elif st.session_state.page == "user_type":

    text = languages[st.session_state.language]
    st.markdown(f"<h2 style='text-align:center;color:#2f7d32'>{text['welcome']}</h2>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button(f"👨‍🌾 {text['farmer']}"):
        st.session_state.page = "farmer"
        st.rerun()
    if c2.button(f"🛒 {text['consumer']}"):
        st.session_state.page = "consumer"
        st.rerun()

# ---------------- FARMER LOGIN ----------------
elif st.session_state.page == "farmer":

    st.markdown("<h2 style='color:#2f7d32'>Farmer Login (OTP)</h2>", unsafe_allow_html=True)
    phone = st.text_input("Mobile Number")

    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.session_id = res["Details"]
                st.success("OTP sent 📲")
            else:
                st.error("OTP sending failed")
        else:
            st.error("Enter valid number")

    if "session_id" in st.session_state:
        otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.session_id}/{otp}"
            result = requests.get(verify_url).json()
            if result["Status"] == "Success":
                st.session_state.page = "farmer_video"
                st.rerun()
            else:
                st.error("Invalid OTP")

# ---------------- FARMER VIDEO VERIFICATION ----------------
elif st.session_state.page == "farmer_video":

    st.markdown("<h3 style='color:#2f7d32'>Live Video Verification</h3>", unsafe_allow_html=True)
    video = st.file_uploader("Upload demo video (mp4/webm)", type=["mp4", "webm"])

    if video:
        os.makedirs("uploads", exist_ok=True)
        with open(f"uploads/verification_{int(time.time())}.mp4", "wb") as f:
            f.write(video.getbuffer())

        st.session_state.farmer_verified = True
        st.success(" Video uploaded & verified (Demo)")
        st.session_state.page = "farmer_dashboard"
        st.rerun()

# ---------------- FARMER DASHBOARD ----------------
elif st.session_state.page == "farmer_dashboard":

    st.markdown("<h2 style='color:#2f7d32'>Farmer Dashboard</h2>", unsafe_allow_html=True)

    if st.session_state.farmer_verified:
        st.success("Verified Farmer ")

    if st.button("Sell Product"):
        st.session_state.page = "product_upload"
        st.rerun()

# ---------------- PRODUCT UPLOAD ----------------
elif st.session_state.page == "product_upload":

    st.markdown("<h3 style='color:#2f7d32'>Upload Product</h3>", unsafe_allow_html=True)

    product = st.text_input("Product Name")
    qty = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price")
    media = st.file_uploader("Upload Image/Video", type=["jpg", "png", "mp4"])

    if st.button("Upload"):
        if product and media:
            os.makedirs("uploads", exist_ok=True)
            with open(f"uploads/{media.name}", "wb") as f:
                f.write(media.getbuffer())
            st.success("Product uploaded successfully ")
            st.session_state.page = "farmer_dashboard"
            st.rerun()
        else:
            st.error("Fill all fields")

# ---------------- CONSUMER ----------------
elif st.session_state.page == "consumer":

    st.markdown("<h2 style='color:#2f7d32;'>Consumer Login</h2>", unsafe_allow_html=True)

    phone = st.text_input("Mobile Number (10 digits)")
    email = st.text_input("Email (Optional)")

    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.consumer_session_id = res["Details"]
                st.success("OTP sent 📲")

    if "consumer_session_id" in st.session_state and not st.session_state.get("consumer_verified", False):
        otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.consumer_session_id}/{otp}"
            verify_res = requests.get(verify_url).json()
            if verify_res["Status"] == "Success":
                st.session_state.consumer_verified = True
                st.success("Consumer Verified ")
                st.rerun()

    # ---------------- CONSUMER DASHBOARD (SAFE) ----------------
    if st.session_state.get("consumer_verified", False):

        st.markdown("## 🛒 Consumer Dashboard")

        uploads = "uploads"
        if os.path.exists(uploads):
            for file in os.listdir(uploads):
                path = os.path.join(uploads, file)
                if file.endswith(".mp4"):
                    st.video(path)
                elif file.endswith((".jpg", ".png")):
                    st.image(path, width=300)
        else:
            st.info("No farmer uploads yet.")

        if st.button("Upload Product for Quality Check"):
            st.session_state.page = "consumer_upload_video"
            st.rerun()

# ---------------- CONSUMER UPLOAD ----------------
elif st.session_state.page == "consumer_upload_video":
    st.markdown("<h3>Upload Product for Quality Check</h3>")
    file = st.file_uploader("Upload Image / Video", type=["mp4", "jpg", "png"])
    if st.button("Upload"):
        if product and file:
            os.makedirs("consumer_uploads", exist_ok=True)
            with open(f"consumer_uploads/{file.name}", "wb") as f:
                f.write(file.getbuffer())
            st.success("Uploaded Successfully ")
            st.session_state.page = "consumer"
            st.rerun()