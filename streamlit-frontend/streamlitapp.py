import streamlit as st
import requests

st.set_page_config(page_title="Fruit Ripeness & Price Detection", layout="wide")

API = "http://127.0.0.1:5000"

# Language translations
TRANSLATIONS = {
    "English": {
        "title": "🍎 Smart Fruit Ripeness & Price Detection",
        "subtitle": "Upload a fruit image OR capture using webcam to detect ripeness & price.",
        "location_options": "📍 Location & Pricing Options",
        "select_district": "Select District",
        "select_market": "Select Market",
        "districts_found": "Found {} districts in the pricing dataset",
        "markets_found": "Found {} markets in {}",
        "no_markets": "No markets found for {}",
        "no_districts": "No districts found in pricing dataset. Using default pricing.",
        "latest_date": "Use Latest Date Only",
        "price_unit": "Price unit",
        "input_mode": "Select input mode:",
        "upload": "Upload",
        "webcam": "Webcam",
        "drag_drop": "Drag and drop an image here, or click to browse",
        "browse_files": "Browse files",
        "predicting": "Predicting...",
        "success": "✅ Prediction Successful!",
        "predicted_image": "Predicted Image",
        "details": "📊 Details:",
        "fruit": "Fruit",
        "grade": "Grade",
        "ripeness": "Ripeness",
        "size": "Size",
        "confidence": "Confidence",
        "price_estimate": "Price Estimate",
        "not_available": "Not available",
        "not_available_filters": "Not available for selected filters",
        "total_counts": "🍎 Total Fruit Counts:",
        "suggestions": "🧭 Suggestions",
        "prediction_failed": "Prediction failed.",
        "failed_fetch_districts": "Failed to fetch districts: {}",
        "failed_fetch_markets": "Failed to fetch markets for {}: {}",
        "district_help": "Choose a district to see available markets and get location-specific pricing",
        "market_help": "Choose a specific market for more accurate pricing",
        "debug_districts": "Debug Districts",
        "debug_info": "Debug Info"
    },
    "Hindi": {
        "title": "🍎 स्मार्ट फल पकने और मूल्य पहचान",
        "subtitle": "फल की छवि अपलोड करें या वेबकैम का उपयोग करके पकने और मूल्य का पता लगाएं।",
        "location_options": "📍 स्थान और मूल्य निर्धारण विकल्प",
        "select_district": "जिला चुनें",
        "select_market": "बाजार चुनें",
        "districts_found": "मूल्य डेटासेट में {} जिले मिले",
        "markets_found": "{} में {} बाजार मिले",
        "no_markets": "{} के लिए कोई बाजार नहीं मिला",
        "no_districts": "मूल्य डेटासेट में कोई जिला नहीं मिला। डिफ़ॉल्ट मूल्य निर्धारण का उपयोग कर रहे हैं।",
        "latest_date": "केवल नवीनतम तिथि का उपयोग करें",
        "price_unit": "मूल्य इकाई",
        "input_mode": "इनपुट मोड चुनें:",
        "upload": "अपलोड",
        "webcam": "वेबकैम",
        "drag_drop": "यहां एक छवि खींचें और छोड़ें, या ब्राउज़ करने के लिए क्लिक करें",
        "browse_files": "फ़ाइलें ब्राउज़ करें",
        "predicting": "भविष्यवाणी कर रहे हैं...",
        "success": "✅ भविष्यवाणी सफल!",
        "predicted_image": "भविष्यवाणी की गई छवि",
        "details": "📊 विवरण:",
        "fruit": "फल",
        "grade": "ग्रेड",
        "ripeness": "पकाव",
        "size": "आकार",
        "confidence": "आत्मविश्वास",
        "price_estimate": "मूल्य अनुमान",
        "not_available": "उपलब्ध नहीं",
        "not_available_filters": "चयनित फ़िल्टर के लिए उपलब्ध नहीं",
        "total_counts": "🍎 कुल फल गिनती:",
        "suggestions": "🧭 सुझाव",
        "prediction_failed": "भविष्यवाणी विफल।",
        "failed_fetch_districts": "जिले प्राप्त करने में विफल: {}",
        "failed_fetch_markets": "{} के लिए बाजार प्राप्त करने में विफल: {}",
        "district_help": "उपलब्ध बाजार देखने और स्थान-विशिष्ट मूल्य निर्धारण के लिए एक जिला चुनें",
        "market_help": "अधिक सटीक मूल्य निर्धारण के लिए एक विशिष्ट बाजार चुनें",
        "debug_districts": "जिले डिबग करें",
        "debug_info": "डिबग जानकारी"
    },
    "Kannada": {
        "title": "🍎 ಸ್ಮಾರ್ಟ್ ಹಣ್ಣು ಪಕ್ವತೆ ಮತ್ತು ಬೆಲೆ ಪತ್ತೆ",
        "subtitle": "ಹಣ್ಣಿನ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ವೆಬ್‌ಕ್ಯಾಮ್ ಬಳಸಿ ಪಕ್ವತೆ ಮತ್ತು ಬೆಲೆಯನ್ನು ಪತ್ತೆ ಮಾಡಿ.",
        "location_options": "📍 ಸ್ಥಳ ಮತ್ತು ಬೆಲೆ ನಿರ್ಧಾರಣಾ ಆಯ್ಕೆಗಳು",
        "select_district": "ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ",
        "select_market": "ಮಾರುಕಟ್ಟೆ ಆಯ್ಕೆಮಾಡಿ",
        "districts_found": "ಬೆಲೆ ಡೇಟಾಸೆಟ್‌ನಲ್ಲಿ {} ಜಿಲ್ಲೆಗಳು ಕಂಡುಬಂದಿವೆ",
        "markets_found": "{} ನಲ್ಲಿ {} ಮಾರುಕಟ್ಟೆಗಳು ಕಂಡುಬಂದಿವೆ",
        "no_markets": "{} ಗಾಗಿ ಯಾವುದೇ ಮಾರುಕಟ್ಟೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ",
        "no_districts": "ಬೆಲೆ ಡೇಟಾಸೆಟ್‌ನಲ್ಲಿ ಯಾವುದೇ ಜಿಲ್ಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಡಿಫಾಲ್ಟ್ ಬೆಲೆ ನಿರ್ಧಾರಣೆಯನ್ನು ಬಳಸುತ್ತಿದ್ದೇವೆ.",
        "latest_date": "ಕೇವಲ ಇತ್ತೀಚಿನ ದಿನಾಂಕವನ್ನು ಬಳಸಿ",
        "price_unit": "ಬೆಲೆ ಘಟಕ",
        "input_mode": "ಇನ್‌ಪುಟ್ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಿ:",
        "upload": "ಅಪ್ಲೋಡ್",
        "webcam": "ವೆಬ್‌ಕ್ಯಾಮ್",
        "drag_drop": "ಇಲ್ಲಿ ಚಿತ್ರವನ್ನು ಎಳೆದು ಬಿಡಿ, ಅಥವಾ ಬ್ರೌಸ್ ಮಾಡಲು ಕ್ಲಿಕ್ ಮಾಡಿ",
        "browse_files": "ಫೈಲ್‌ಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ",
        "predicting": "ಭವಿಷ್ಯವಾಣಿ ಮಾಡುತ್ತಿದ್ದೇವೆ...",
        "success": "✅ ಭವಿಷ್ಯವಾಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ!",
        "predicted_image": "ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿದ ಚಿತ್ರ",
        "details": "📊 ವಿವರಗಳು:",
        "fruit": "ಹಣ್ಣು",
        "grade": "ಗ್ರೇಡ್",
        "ripeness": "ಪಕ್ವತೆ",
        "size": "ಗಾತ್ರ",
        "confidence": "ಆತ್ಮವಿಶ್ವಾಸ",
        "price_estimate": "ಬೆಲೆ ಅಂದಾಜು",
        "not_available": "ಲಭ್ಯವಿಲ್ಲ",
        "not_available_filters": "ಆಯ್ಕೆಮಾಡಿದ ಫಿಲ್ಟರ್‌ಗಳಿಗೆ ಲಭ್ಯವಿಲ್ಲ",
        "total_counts": "🍎 ಒಟ್ಟು ಹಣ್ಣು ಎಣಿಕೆ:",
        "suggestions": "🧭 ಸಲಹೆಗಳು",
        "prediction_failed": "ಭವಿಷ್ಯವಾಣಿ ವಿಫಲವಾಗಿದೆ.",
        "failed_fetch_districts": "ಜಿಲ್ಲೆಗಳನ್ನು ಪಡೆಯಲು ವಿಫಲ: {}",
        "failed_fetch_markets": "{} ಗಾಗಿ ಮಾರುಕಟ್ಟೆಗಳನ್ನು ಪಡೆಯಲು ವಿಫಲ: {}",
        "district_help": "ಲಭ್ಯವಿರುವ ಮಾರುಕಟ್ಟೆಗಳನ್ನು ನೋಡಲು ಮತ್ತು ಸ್ಥಳ-ನಿರ್ದಿಷ್ಟ ಬೆಲೆ ನಿರ್ಧಾರಣೆಗಾಗಿ ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "market_help": "ಹೆಚ್ಚು ನಿಖರವಾದ ಬೆಲೆ ನಿರ್ಧಾರಣೆಗಾಗಿ ನಿರ್ದಿಷ್ಟ ಮಾರುಕಟ್ಟೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "debug_districts": "ಜಿಲ್ಲೆಗಳನ್ನು ಡಿಬಗ್ ಮಾಡಿ",
        "debug_info": "ಡಿಬಗ್ ಮಾಹಿತಿ"
    }
}

# Language selection
selected_language = st.selectbox("🌐 Language / भाषा / ಭಾಷೆ", list(TRANSLATIONS.keys()), index=0)
t = TRANSLATIONS[selected_language]

st.title(t["title"])
st.markdown(t["subtitle"])

@st.cache_data(ttl=300)
def fetch_districts():
    try:
        r = requests.get(f"{API}/pricing/options", timeout=10)
        r.raise_for_status()
        return r.json().get("districts", [])
    except Exception as e:
        st.error(t["failed_fetch_districts"].format(e))
        return []

@st.cache_data(ttl=300)
def fetch_markets(district: str):
    if not district:
        return []
    try:
        r = requests.get(f"{API}/pricing/options", params={"district": district}, timeout=10)
        r.raise_for_status()
        return r.json().get("markets", [])
    except Exception as e:
        st.error(t["failed_fetch_markets"].format(district, e))
        return []

def post_predict(image_bytes, district: str|None, market: str|None, latest_only: bool):
    files = {"image": ("upload.jpg", image_bytes, "image/jpeg")}
    data = {}
    if district:
        data["district"] = district
    if market:
        data["market"] = market
    data["latest_only"] = "true" if latest_only else "false"
    return requests.post(f"{API}/predict", files=files, data=data, timeout=60)

# Location filters
st.markdown(f"### {t['location_options']}")
districts = fetch_districts()
if districts:
    st.info(t["districts_found"].format(len(districts)))
    district = st.selectbox(t["select_district"], [""] + districts, index=0, help=t["district_help"])
    markets = fetch_markets(district) if district else []
    if markets:
        st.info(t["markets_found"].format(len(markets), district))
        market = st.selectbox(t["select_market"], [""] + markets, index=0, help=t["market_help"])
    else:
        market = ""
        if district:
            st.warning(t["no_markets"].format(district))
else:
    st.warning(t["no_districts"])
    district = ""
    market = ""

latest_only = st.toggle(t["latest_date"], value=True)
price_unit = st.radio(t["price_unit"], ["Rs/Quintal", "Rs/kg"], horizontal=True)

# Debug section
with st.expander(t["debug_info"]):
    if st.button(t["debug_districts"]):
        try:
            debug_response = requests.get(f"{API}/debug/districts", timeout=10)
            if debug_response.status_code == 200:
                debug_data = debug_response.json()
                st.json(debug_data)
            else:
                st.error(f"Debug request failed: {debug_response.status_code}")
        except Exception as e:
            st.error(f"Debug error: {e}")

# Input mode
input_mode = st.radio(t["input_mode"], [t["upload"], t["webcam"]], horizontal=True)

# Helpers for auto-run on new file
import hashlib
if "last_file_key" not in st.session_state:
    st.session_state["last_file_key"] = None
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

def compute_key(content_bytes: bytes) -> str:
    return hashlib.sha1(content_bytes).hexdigest()

def render_result(data: dict, unit: str):
    st.success(t["success"])
    pred_image_url = data.get("image")
    predictions = data.get("predictions", [])
    fruit_counts = data.get("fruit_counts", {})
    col1, col2 = st.columns([2, 1])
    with col1:
        if pred_image_url:
            ts = str(int(time.time()*1000))
            st.image(f"{API}/{pred_image_url}?_cb={ts}", caption=t["predicted_image"], use_container_width=True)
    with col2:
        st.markdown(f"### {t['details']}")
        if predictions:
            for pred in predictions:
                st.write(f"**{t['fruit']}**: `{pred.get('fruit','')}`")
                st.write(f"**{t['grade']}**: `{pred.get('grade','')}`")
                st.write(f"**{t['ripeness']}**: `{pred.get('ripeness','')}`")
                st.write(f"**{t['size']}**: `{pred.get('size','')}`")
                st.write(f"**{t['confidence']}**: `{pred.get('confidence','')}`")
                if 'price' in pred:
                    try:
                        base_price = float(pred['price'])
                    except Exception:
                        base_price = None
                    if base_price is not None:
                        shown = round(base_price / 100.0, 2) if unit == "Rs/kg" else round(base_price, 2)
                        st.write(f"**{t['price_estimate']}** ({unit}): ₹ `{shown}`")
                    else:
                        st.write(f"**{t['price_estimate']}**: {t['not_available']}")
                else:
                    st.write(f"**{t['price_estimate']}**: {t['not_available_filters']}")
                st.write("---")
        else:
            st.write("No predictions returned.")
        if fruit_counts:
            st.markdown(f"### {t['total_counts']}")
            for fruit, count in fruit_counts.items():
                st.write(f"**{fruit.capitalize()}**: {count}")
        suggestions = data.get("suggestions")
        if suggestions:
            st.markdown(f"### {t['suggestions']}")
            if suggestions.get("districts"):
                st.write({"districts": suggestions["districts"]})
            if suggestions.get("markets"):
                st.write({"markets": suggestions["markets"]})

image_file = None
if input_mode == t["upload"]:
    # Enhanced drag and drop file uploader with custom styling
    st.markdown(f"""
    <style>
    .uploadedFile {{
        display: none;
    }}
    .stFileUploader > div {{
        width: 100%;
    }}
    .stFileUploader > div > div {{
        width: 100%;
    }}
    .stFileUploader > div > div > div {{
        width: 100%;
    }}
    .stFileUploader > div > div > div > div {{
        width: 100%;
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #f8f9fa;
        transition: border-color 0.3s ease;
    }}
    .stFileUploader > div > div > div > div:hover {{
        border-color: #007bff;
        background-color: #e3f2fd;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    image_file = st.file_uploader(
        t["drag_drop"], 
        type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
        help=t["browse_files"],
        label_visibility="collapsed"
    )
    
    # Add visual feedback for drag and drop
    if image_file is None:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px dashed #cccccc; border-radius: 10px; background-color: #f8f9fa; margin: 10px 0;">
            <p style="margin: 0; color: #666; font-size: 16px;">📁 {t['drag_drop']}</p>
            <p style="margin: 5px 0 0 0; color: #999; font-size: 12px;">Supported: JPG, PNG, BMP, TIFF, WebP</p>
        </div>
        """, unsafe_allow_html=True)
else:
    image_file = st.camera_input(t["webcam"] + " an image")

if image_file is not None:
    content_bytes = image_file.getvalue()
    key = compute_key(content_bytes)
    # Auto-run prediction when the uploaded/captured file changes
    if key != st.session_state["last_file_key"]:
        st.session_state["last_file_key"] = key
        with st.spinner(t["predicting"]):
            resp = post_predict(content_bytes, district or None, market or None, latest_only)
            if resp.status_code == 200:
                st.session_state["last_result"] = resp.json()
            else:
                try:
                    st.session_state["last_result"] = resp.json()
                except Exception:
                    st.session_state["last_result"] = {"error": f"Status {resp.status_code}", "message": resp.text}

# Bust browser image caching by appending a cache-busting query param when rendering
import time

# Render last result (if any)
if st.session_state["last_result"] is not None:
    data = st.session_state["last_result"]
    if isinstance(data, dict) and data.get("success") or ("predictions" in data or "image" in data):
        render_result(data, price_unit)
    else:
        st.error(t["prediction_failed"])
        try:
            st.json(data)
        except Exception:
            st.write(data)
