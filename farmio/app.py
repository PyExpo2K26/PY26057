from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests

app = Flask(__name__)
app.secret_key = "farmio_aesthetic_2026"

# 1. Full Translation Dictionary
TRANSLATIONS = {
    "English": {
        "welcome": "Welcome to FARMIO", "farmer": "Farmer", "consumer": "Consumer",
        "otp_title": "Login Verification", "phone_label": "Enter Mobile Number",
        "send_otp": "Send OTP", "verify_btn": "Verify & Continue",
        "face_title": "Step 1: Live Face Verification", "field_title": "Step 2: Live Field Verification",
        "upload_demo": "Upload Demo Video", "tagline": "Welcome back, Soil Warrior! 🌾"
    },
    "Tamil": {
        "welcome": "FARMIO-க்கு வரவேற்கிறோம்", "farmer": "விவசாயி", "consumer": "நுகர்வோர்",
        "otp_title": "உள்நுழைவு சரிபார்ப்பு", "phone_label": "கைபேசி எண்ணை உள்ளிடவும்",
        "send_otp": "OTP அனுப்பவும்", "verify_btn": "சரிபார்த்து தொடரவும்",
        "face_title": "படி 1: நேரடி முக சரிபார்ப்பு", "field_title": "படி 2: நேரடி பண்ணை சரிபார்ப்பு",
        "upload_demo": "டெமோ வீடியோவை பதிவேற்றவும்", "tagline": "மீண்டும் வருக, மண்ணின் மைந்தனே! 🌾"
    },
    "Malayalam": {
        "welcome": "FARMIO-യിലേക്ക് സ്വാഗതം", "farmer": "കർഷകൻ", "consumer": "ഉപഭോക്താവ്",
        "otp_title": "ലോഗിൻ വെരിഫിക്കേഷൻ", "phone_label": "മൊബൈൽ നമ്പർ നൽകുക",
        "send_otp": "OTP അയക്കുക", "verify_btn": "പരിശോധിച്ച് തുടരുക",
        "face_title": "ഘട്ടം 1: ഫെയ്സ് വെരിഫിക്കേഷൻ", "field_title": "ഘട്ടം 2: ഫീల్ഡ് വെരിഫിക്കേഷൻ",
        "tagline": "സ്വാഗതം, മണ്ണിന്റെ മകനേ! 🌾"
    },
    "Telugu": {
        "welcome": "FARMIO కి స్వాగతం", "farmer": "రైతు", "consumer": "వినియోగదారు",
        "otp_title": "లాగిన్ ధృవీకరణ", "phone_label": "మొబైల్ నంబర్ నమోదు చేయండి",
        "send_otp": "OTP పంపండి", "verify_btn": "ధృవీకరించి కొనసాగండి",
        "face_title": "దశ 1: ముఖ ధృవీకరణ", "field_title": "దశ 2: క్షేత్ర ధృవీకరణ",
        "tagline": "స్వాగతం, రైతు సోదరా! 🌾"
    },
    "Marathi": {
        "welcome": "FARMIO मध्ये आपले स्वागत आहे", "farmer": "शेतकरी", "consumer": "ग्राहक",
        "otp_title": "लॉगिन सत्यापन", "phone_label": "मोबाईल नंबर टाका",
        "send_otp": "OTP पाठवा", "verify_btn": "सत्यापित करा",
        "face_title": "टप्पा १: चेहरा पडताळणी", "field_title": "टप्पा २: शेत पडताळणी",
        "tagline": "स्वागत आहे, बळीराजा! 🌾"
    },
    "Hindi": {
        "welcome": "FARMIO में आपका स्वागत है", "farmer": "किसान", "consumer": "उपभोक्ता",
        "otp_title": "लॉगिन सत्यापन", "phone_label": "मोबाइल नंबर दर्ज करें",
        "send_otp": "ओटीपी भेजें", "verify_btn": "सत्यापित करें",
        "face_title": "चरण 1: चेहरा सत्यापन", "field_title": "चरण 2: खेत सत्यापन",
        "tagline": "स्वागत है, अन्नदाता! 🌾"
    },
    "Kannada": {
        "welcome": "FARMIO ಗೆ ಸ್ವಾಗత", "farmer": "ರೈತ", "consumer": "ಗ್ರಾಹಕ",
        "otp_title": "ಲಾಗಿನ್ ಪರಿಶೀಲನೆ", "phone_label": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ",
        "send_otp": "OTP ಕಳುಹಿಸಿ", "verify_btn": "ಪರಿಶೀಲಿಸಿ ಮುಂದುವರಿಯಿರಿ",
        "face_title": "ಹಂತ 1: ಮುಖದ ಪರಿಶೀಲನೆ", "field_title": "ಹಂತ 2: ಜಮೀನು ಪರಿಶೀಲನೆ",
        "tagline": "ಸ್ವಾಗತ, ರೈತ ಮಿತ್ರನೇ! 🌾"
    },
    "Bengali": {
        "welcome": "FARMIO তে আপনাকে স্বাগতম", "farmer": "কৃষক", "consumer": "ভোক্তা",
        "otp_title": "লগইন যাচাইকরণ", "phone_label": "মোবাইল নম্বর লিখুন",
        "send_otp": "ওটিপি পাঠান", "verify_btn": "যাচাই করে এগিয়ে যান",
        "face_title": "ধাপ ১: মুখ যাচাইকরণ", "field_title": "ধাপ ২: জমি যাচাইকরণ",
        "tagline": "স্বাগতম, মাটির সন্তান! 🌾"
    },
    "Gujarati": {
        "welcome": "FARMIO માં આપનું સ્વાગત છે", "farmer": "ખેડૂત", "consumer": "ગ્રાહક",
        "otp_title": "લોગિન ચકાસણી", "phone_label": "મોબાઇલ નંબર દાખલ કરો",
        "send_otp": "OTP મોકલો", "verify_btn": "ચકાસો અને આગળ વધો",
        "face_title": "પગલું ૧: ચહેરો ચકાસણી", "field_title": "પગલું ૨: ખેતર ચકાસણી",
        "tagline": "સ્વાગત છે, ખેડૂત પુત્ર! 🌾"
    },
    "Punjabi": {
        "welcome": "FARMIO ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ", "farmer": "ਕਿਸਾਨ", "consumer": "ਗ੍ਰਾਹਕ",
        "otp_title": "ਲੌਗਇਨ ਤਸਦੀਕ", "phone_label": "ਮੋਬਾਈਲ ਨੰਬਰ ਦਰਜ ਕਰੋ",
        "send_otp": "OTP ਭੇਜੋ", "verify_btn": "ਤਸਦੀਕ ਕਰੋ",
        "face_title": "ਪੜਾਅ 1: ਚਿਹਰਾ ਤਸਦੀਕ", "field_title": "ਪੜਾਅ 2: ਖੇਤ ਤਸਦੀਕ",
        "tagline": "ਜੀ ਆਇਆਂ ਨੂੰ, ਅੰਨਦਾਤਾ ਜੀ! 🌾"
    },
    "Bhojpuri": {
        "welcome": "FARMIO में राउर स्वागत बा", "farmer": "किसान", "consumer": "ग्राहक",
        "otp_title": "लॉगिन जांच", "phone_label": "मोबाइल नंबर डालीं",
        "send_otp": "OTP भेजीं", "verify_btn": "जांच करीं",
        "face_title": "पहिलका चरण: चेहरा जांच", "field_title": "दूसरका चरण: खेत जांच",
        "tagline": "राउर स्वागत बा, किसान भाई! 🌾"
    },
    "Urdu": {
        "welcome": "FARMIO میں خوش آمدید", "farmer": "کسان", "consumer": "صارف",
        "otp_title": "لاگ ان تصدیق", "phone_label": "موبائل نمبر درج کریں",
        "send_otp": "او ٹی پی بھیجیں", "verify_btn": "تصدیق کریں",
        "face_title": "مرحلہ 1: چہرے کی تصدیق", "field_title": "مرحلہ 2: کھیت کی تصدیق",
        "tagline": "خوش آمدید، کسان بھائی! 🌾"
    },
    "Assamese": {
        "welcome": "FARMIO ত আপোনাক স্বাগতম", "farmer": "কৃষক", "consumer": "গ্ৰাহক",
        "otp_title": "লগইন সত্যপন", "phone_label": "মবাইল নম্বৰ লিখক",
        "send_otp": "OTP পঠাওক", "verify_btn": "সত্যপন কৰি আগবাঢ়ক",
        "face_title": "স্তৰ ১: মুখৰ সত্যপন", "field_title": "স্তৰ ২: পথাৰৰ সত্যপন",
        "tagline": "স্বাগতম, হে ধৰিত্ৰীৰ সন্তান! 🌾"
    },
    "Rajasthani": {
        "welcome": "FARMIO में थांरो स्वागत है", "farmer": "खेतीहर", "consumer": "ग्राहक",
        "otp_title": "लॉगिन जांच", "phone_label": "मोबाइल नंबर लिखो",
        "send_otp": "OTP भेजो", "verify_btn": "जांच पक्की करो",
        "face_title": "चरण 1: मूंढो जांच", "field_title": "चरण 2: खेत जांच",
        "tagline": "घणो मान, धोरां रा सपूत! 🌾"
    }
}

# 2. Automation: Inject text into every page
@app.context_processor
def inject_translations():
    lang = session.get('lang', 'English')
    # If the selected language is missing in the dict, fall back to English
    lang_data = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    return dict(text=lang_data)

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/language', methods=['GET', 'POST'])
def language_selection():
    if request.method == 'POST':
        session['lang'] = request.form.get('lang')
        return redirect(url_for('user_type'))
    return render_template('language.html', langs=TRANSLATIONS)

@app.route('/user_type')
def user_type():
    return render_template('user_type.html')

@app.route('/verify/otp/<role>', methods=['GET', 'POST'])
def verify_otp(role):
    msg = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        otp_entered = request.form.get('otp')

        if phone and not otp_entered:
            # API Call Logic here...
            msg = "OTP Sent!"
        
        if otp_entered == "123456": # Standard Test OTP
            if role == 'farmer':
                return redirect(url_for('verify_face'))
            return redirect(url_for('consumer_dashboard'))
    return render_template('verify_otp.html', role=role, msg=msg)

@app.route('/verify/face')
def verify_face():
    return render_template('verify_face.html')

@app.route('/verify/field')
def verify_field():
    return render_template('verify_field.html')

@app.route('/dashboard/farmer')
def farmer_dashboard():
    return render_template('dashboard.html', role='farmer')

@app.route('/dashboard/consumer')
def consumer_dashboard():
    return render_template('dashboard.html', role='consumer')

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)