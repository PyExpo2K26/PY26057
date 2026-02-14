import streamlit as st
import time
import requests
import os
import numpy as np
import cv2
from ultralytics import YOLO

# Load CV model once
cv_model = YOLO("models/best.pt")

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

    "English": {
        "welcome": "Welcome to FARMIO",
        "farmer": "Farmer",
        "consumer": "Consumer",
        "select_lang": "Select Language",
        "consumer_login": "Consumer Login (OTP)",
        "mobile_10": "Mobile Number (10 digits)",
        "phone": "Mobile Number",
        "farmer_login": "Farmer Login (OTP)",
        "send_otp": "Send OTP",
        "enter_otp": "Enter OTP",
        "verify_otp": "Verify OTP",
        "face_step": "Step 1: FACE (Live Required)",
        "field_step": "Step 2: FIELD",
        "quality": "Quality Score",
        "sell": "Sell Product",
        "history": "Verification History",
        "profile": "Profile & Settings",
        "logout": "Logout"
    },

    "Tamil": {
        "welcome": "FARMIO-க்கு வரவேற்கிறோம்",
        "farmer": "விவசாயி",
        "consumer": "நுகர்வோர்",
        "select_lang": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "consumer_login": "நுகர்வோர் உள்நுழைவு (OTP)",
        "mobile_10": "கைபேசி எண் (10 இலக்கங்கள்)",
        "phone": "கைபேசி எண்",
        "send_otp": "OTP அனுப்பவும்",
        "enter_otp": "OTP-ஐ உள்ளிடவும்",
        "verify_otp": "OTP-ஐ சரிபார்க்கவும்",
        "farmer_login": "விவசாயி உள்நுழைவு (OTP)",
        "face_step": "படி 1: முகம் சரிபார்ப்பு",
        "field_step": "படி 2: நிலம் சரிபார்ப்பு",
        "quality": "தர மதிப்பீடு",
        "sell": "பொருளை விற்பனை செய்",
        "history": "சரிபார்ப்பு வரலாறு",
        "profile": "சுயவிவரம்",
        "logout": "வெளியேறு"
    },

    "Hindi": {
        "welcome": "FARMIO में आपका स्वागत है",
        "farmer": "किसान",
        "consumer": "उपभोक्ता",
        "select_lang": "भाषा चुनें",
        "consumer_login": "उपभोक्ता लॉगिन (OTP)",
        "mobile_10": "मोबाइल नंबर (10 अंक)",
        "phone": "मोबाइल नंबर",
        "send_otp": "ओटीपी भेजें",
        "enter_otp": "ओटीपी दर्ज करें",
        "farmer_login": "किसान लॉगिन (ओटीपी)",
        "verify_otp": "ओटीपी सत्यापित करें",
        "face_step": "चरण 1: चेहरा सत्यापन",
        "field_step": "चरण 2: खेत सत्यापन",
        "quality": "गुणवत्ता स्कोर",
        "sell": "उत्पाद बेचें",
        "history": "सत्यापन इतिहास",
        "profile": "प्रोफ़ाइल और सेटिंग्स",
        "logout": "लॉग आउट"
    },

    "Malayalam": {
        "welcome": "FARMIO ലേക്ക് സ്വാഗതം",
        "farmer": "കർഷകൻ",
        "consumer": "ഉപഭോക്താവ്",
        "select_lang": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "consumer_login": "ഉപഭോക്തൃ ലോഗിൻ (OTP)",
        "mobile_10": "മൊബൈൽ നമ്പർ (10 അക്കങ്ങൾ)",
        "phone": "മൊബൈൽ നമ്പർ",
        "send_otp": "OTP അയയ്ക്കുക",
        "enter_otp": "OTP നൽകുക",
        "verify_otp": "OTP സ്ഥിരീകരിക്കുക",
        "farmer_login": "കർഷക ലോഗിൻ (OTP)",
        "face_step": "പടി 1: മുഖം സ്ഥിരീകരണം",
        "field_step": "പടി 2: വയൽ സ്ഥിരീകരണം",
        "quality": "ഗുണനിലവാര സ്കോർ",
        "sell": "ഉൽപ്പന്നം വിൽക്കുക",
        "history": "സ്ഥിരീകരണ ചരിത്രം",
        "profile": "പ്രൊഫൈൽ & ക്രമീകരണങ്ങൾ",
        "logout": "ലോഗ് ഔട്ട്"
    },

    "Telugu": {
        "welcome": "FARMIO కు స్వాగతం",
        "farmer": "రైతు",
        "consumer": "వినియోగదారు",
        "select_lang": "భాషను ఎంచుకోండి",
        "consumer_login": "వినియోగదారు లాగిన్ (OTP)",
        "mobile_10": "మొబైల్ నంబర్ (10 అంకెలు)",
        "phone": "మొబైల్ నంబర్",
        "send_otp": "OTP పంపండి",
        "enter_otp": "OTP నమోదు చేయండి",
        "verify_otp": "OTP ధృవీకరించండి",
        "face_step": "దశ 1: ముఖ ధృవీకరణ",
        "field_step": "దశ 2: పొలం ధృవీకరణ",
        "quality": "నాణ్యత స్కోర్",
        "sell": "ఉత్పత్తి అమ్మండి",
        "history": "ధృవీకరణ చరిత్ర",
        "profile": "ప్రొఫైల్ & సెట్టింగ్స్",
        "logout": "లాగ్ అవుట్"
    },

    "Kannada": {
        "welcome": "FARMIO ಗೆ ಸ್ವಾಗತ",
        "farmer": "ರೈತ",
        "consumer": "ಗ್ರಾಹಕ",
        "select_lang": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "consumer_login": "ಗ್ರಾಹಕ ಲಾಗಿನ್ (OTP)",
        "mobile_10": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (10 ಅಂಕೆಗಳು)",
        "phone": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        "send_otp": "OTP ಕಳುಹಿಸಿ",
        "enter_otp": "OTP ನಮೂದಿಸಿ",
        "verify_otp": "OTP ಪರಿಶೀಲಿಸಿ",
        "face_step": "ಹಂತ 1: ಮುಖ ಪರಿಶೀಲನೆ",
        "field_step": "ಹಂತ 2: ಹೊಲ ಪರಿಶೀಲನೆ",
        "quality": "ಗುಣಮಟ್ಟದ ಅಂಕ",
        "sell": "ಉತ್ಪನ್ನ ಮಾರಾಟ",
        "history": "ಪರಿಶೀಲನೆ ಇತಿಹಾಸ",
        "profile": "ಪ್ರೊಫೈಲ್ & ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "logout": "ಲಾಗ್ ಔಟ್"
    },

    "Marathi": {
        "welcome": "FARMIO मध्ये आपले स्वागत आहे",
        "farmer": "शेतकरी",
        "consumer": "ग्राहक",
        "select_lang": "भाषा निवडा",
        "consumer_login": "ग्राहक लॉगिन (OTP)",
        "mobile_10": "मोबाईल क्रमांक (10 अंक)",
        "phone": "मोबाईल क्रमांक",
        "send_otp": "OTP पाठवा",
        "enter_otp": "OTP टाका",
        "verify_otp": "OTP तपासा",
        "face_step": "पायरी 1: चेहरा तपासणी",
        "field_step": "पायरी 2: शेत तपासणी",
        "quality": "गुणवत्ता गुण",
        "sell": "उत्पादन विक्री",
        "history": "तपासणी इतिहास",
        "profile": "प्रोफाइल आणि सेटिंग्स",
        "logout": "लॉग आऊट"
    },

    "Bengali": {
        "welcome": "FARMIO তে স্বাগতম",
        "farmer": "কৃষক",
        "consumer": "ভোক্তা",
        "select_lang": "ভাষা নির্বাচন করুন",
        "consumer_login": "ভোক্তা লগইন (OTP)",
        "mobile_10": "মোবাইল নম্বর (10 সংখ্যা)",
        "phone": "মোবাইল নম্বর",
        "send_otp": "OTP পাঠান",
        "enter_otp": "OTP লিখুন",
        "verify_otp": "OTP যাচাই করুন",
        "face_step": "ধাপ ১: মুখ যাচাই",
        "field_step": "ধাপ ২: ক্ষেত যাচাই",
        "quality": "গুণমান স্কোর",
        "sell": "পণ্য বিক্রি করুন",
        "history": "যাচাইকরণ ইতিহাস",
        "profile": "প্রোফাইল ও সেটিংস",
        "logout": "লগ আউট"
    },

    "Gujarati": {
        "welcome": "FARMIO માં આપનું સ્વાગત છે",
        "farmer": "ખેડૂત",
        "consumer": "ગ્રાહક",
        "select_lang": "ભાષા પસંદ કરો",
        "consumer_login": "ગ્રાહક લોગિન (OTP)",
        "mobile_10": "મોબાઇલ નંબર (10 અંક)",
        "phone": "મોબાઇલ નંબર",
        "send_otp": "OTP મોકલો",
        "enter_otp": "OTP દાખલ કરો",
        "verify_otp": "OTP ચકાસો",
        "face_step": "પગલું 1: ચહેરો ચકાસણી",
        "field_step": "પગલું 2: ખેતર ચકાસણી",
        "quality": "ગુણવત્તા સ્કોર",
        "sell": "ઉત્પાદન વેચો",
        "history": "ચકાસણી ઇતિહાસ",
        "profile": "પ્રોફાઇલ અને સેટિંગ્સ",
        "logout": "લોગ આઉટ"
    },

    "Punjabi": {
        "welcome": "FARMIO ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ",
        "farmer": "ਕਿਸਾਨ",
        "consumer": "ਖਪਤਕਾਰ",
        "select_lang": "ਭਾਸ਼ਾ ਚੁਣੋ",
        "consumer_login": "ਖਪਤਕਾਰ ਲੌਗਿਨ (OTP)",
        "mobile_10": "ਮੋਬਾਈਲ ਨੰਬਰ (10 ਅੰਕ)",
        "phone": "ਮੋਬਾਈਲ ਨੰਬਰ",
        "send_otp": "OTP ਭੇਜੋ",
        "enter_otp": "OTP ਦਰਜ ਕਰੋ",
        "verify_otp": "OTP ਤਸਦੀਕ ਕਰੋ",
        "face_step": "ਕਦਮ 1: ਚਿਹਰਾ ਤਸਦੀਕ",
        "field_step": "ਕਦਮ 2: ਖੇਤ ਤਸਦੀਕ",
        "quality": "ਗੁਣਵੱਤਾ ਸਕੋਰ",
        "sell": "ਉਤਪਾਦ ਵੇਚੋ",
        "history": "ਤਸਦੀਕ ਇਤਿਹਾਸ",
        "profile": "ਪ੍ਰੋਫਾਈਲ ਅਤੇ ਸੈਟਿੰਗਸ",
        "logout": "ਲੌਗ ਆਉਟ"
    },

    "Urdu": {
        "welcome": "FARMIO میں خوش آمدید",
        "farmer": "کسان",
        "consumer": "صارف",
        "select_lang": "زبان منتخب کریں",
        "consumer_login": "صارف لاگ ان (OTP)",
        "mobile_10": "موبائل نمبر (10 ہندسے)",
        "phone": "موبائل نمبر",
        "send_otp": "OTP بھیجیں",
        "enter_otp": "OTP درج کریں",
        "verify_otp": "OTP تصدیق کریں",
        "face_step": "مرحلہ 1: چہرہ تصدیق",
        "field_step": "مرحلہ 2: کھیت تصدیق",
        "quality": "معیار اسکور",
        "sell": "مصنوعات فروخت کریں",
        "history": "تصدیق کی تاریخ",
        "profile": "پروفائل اور سیٹنگز",
        "logout": "لاگ آؤٹ"
    },

    "Odia": {
        "welcome": "FARMIO କୁ ସ୍ୱାଗତ",
        "farmer": "ଚାଷୀ",
        "consumer": "ଉପଭୋକ୍ତା",
        "select_lang": "ଭାଷା ଚୟନ କରନ୍ତୁ",
        "consumer_login": "ଉପଭୋକ୍ତା ଲଗଇନ (OTP)",
        "mobile_10": "ମୋବାଇଲ ନମ୍ବର (10 ଅଙ୍କ)",
        "phone": "ମୋବାଇଲ ନମ୍ବର",
        "send_otp": "OTP ପଠାନ୍ତୁ",
        "enter_otp": "OTP ଦିଅନ୍ତୁ",
        "verify_otp": "OTP ସତ୍ୟାପନ କରନ୍ତୁ",
        "face_step": "ପଦକ୍ରମ 1: ମୁହଁ ସତ୍ୟାପନ",
        "field_step": "ପଦକ୍ରମ 2: କ୍ଷେତ୍ର ସତ୍ୟାପନ",
        "quality": "ଗୁଣମାନ ସ୍କୋର",
        "sell": "ପଣ୍ୟ ବିକ୍ରୟ",
        "history": "ସତ୍ୟାପନ ଇତିହାସ",
        "profile": "ପ୍ରୋଫାଇଲ ଓ ସେଟିଂସ",
        "logout": "ଲଗ୍ ଆଉଟ୍"
    },

    "Assamese": {
        "welcome": "FARMIO লৈ স্বাগতম",
        "farmer": "খেতিয়ক",
        "consumer": "গ্ৰাহক",
        "select_lang": "ভাষা বাছনি কৰক",
        "consumer_login": "গ্ৰাহক লগইন (OTP)",
        "mobile_10": "মোবাইল নম্বৰ (10 সংখ্যা)",
        "phone": "মোবাইল নম্বৰ",
        "send_otp": "OTP পঠিয়াওক",
        "enter_otp": "OTP প্ৰৱেশ কৰক",
        "verify_otp": "OTP নিশ্চিত কৰক",
        "face_step": "পদক্ষেপ ১: মুখ নিশ্চিতকৰণ",
        "field_step": "পদক্ষেপ ২: ক্ষেত্ৰ নিশ্চিতকৰণ",
        "quality": "গুণমান স্কোৰ",
        "sell": "পণ্য বিক্ৰী কৰক",
        "history": "নিশ্চিতকৰণ ইতিহাস",
        "profile": "প্ৰ'ফাইল আৰু ছেটিংছ",
        "logout": "লগ আউট"
    },

    "Rajasthani": {
        "welcome": "FARMIO में थारो स्वागत है",
        "farmer": "किसान",
        "consumer": "ग्राहक",
        "select_lang": "भाषा चुनो",
        "consumer_login": "ग्राहक लॉगिन (OTP)",
        "mobile_10": "मोबाइल नंबर (10 अंक)",
        "phone": "मोबाइल नंबर",
        "send_otp": "OTP भेजो",
        "enter_otp": "OTP भरो",
        "verify_otp": "OTP जांचो",
        "face_step": "चरण 1: चेहरा जांच",
        "field_step": "चरण 2: खेत जांच",
        "quality": "गुणवत्ता स्कोर",
        "sell": "उत्पाद बेचो",
        "history": "जांच इतिहास",
        "profile": "प्रोफाइल और सेटिंग्स",
        "logout": "लॉग आउट"
    },
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
# ---------------- TRANSLATION FUNCTION ----------------
def L(key):
    lang = st.session_state.get("language", "English")
    return languages.get(lang, languages["English"]).get(key, key)


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

    # Loop through languages dictionary (safer)
    for i, lang in enumerate(languages.keys()):
        native_label = native_names.get(lang, lang)

        if cols[i % 3].button(native_label):
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
    st.header(L("farmer_login"))

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

    st.subheader("Product Detection")

    farmer_img = st.file_uploader("Upload fruit / vegetable image", type=["jpg","png","jpeg"], key="farmer_upload")

    if farmer_img:
        st.image(farmer_img, width=250)

        # Save temporarily
        temp_path = f"uploads/{farmer_img.name}"
        with open(temp_path, "wb") as f:
            f.write(farmer_img.getbuffer())

        results = cv_model(temp_path)
        plotted = results[0].plot()

        st.image(plotted, caption="Detection Result")

    if st.button("Sell Product"):
        st.session_state.page = "product_upload"
        st.rerun()

# ---------------- CONSUMER LOGIN ----------------
elif st.session_state.page == "consumer_login":
    st.header(L("consumer_login"))
    phone = st.text_input(L("mobile_10"))

    if st.button(L("send_otp")):

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

            temp_path = f"uploads/{uploaded.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded.getbuffer())

            results = cv_model(temp_path)

            plotted = results[0].plot()
            st.image(plotted, caption="Detection Result")

            # confidence score
            conf = 0
            for r in results:
                if len(r.boxes) > 0:
                    conf = float(r.boxes.conf.max())

            score = int(conf * 100)
            st.metric("Quality Score", f"{score} / 100")

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


    
   








