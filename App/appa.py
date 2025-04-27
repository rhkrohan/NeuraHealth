# pneumo_ui.py – Streamlit Medical Diagnosis Simulator
import time
import random
import base64
import pathlib
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# 0 · Page Config
st.set_page_config(
    page_title="Neura Health Simulator",
    page_icon="⚕️",
    layout="wide"
)

# 1 · Inline the JPG background
BG_PATH = pathlib.Path(__file__).parent / "bg.jpg"
if not BG_PATH.exists():
    raise FileNotFoundError(f"Could not find background image at {BG_PATH}")
bg_bytes = BG_PATH.read_bytes()
bg_b64 = base64.b64encode(bg_bytes).decode()

# 2 · Custom CSS
st.markdown(f"""
<style>
/* Background */
[data-testid="stAppViewContainer"] {{
  background-image: url("data:image/jpeg;base64,{bg_b64}");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  box-shadow: inset 0 0 200px rgba(0,0,0,0.4);
}}
[data-testid="stAppViewContainer"]::before {{
  content: '';
  position: absolute;
  inset: 0;
  backdrop-filter: blur(6px);
  background: rgba(0,0,0,0.55);
  z-index: -1;
}}

/* Typography */
body, p {{
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #eee;
}}
h1 {{ font-size: 3.2rem; margin-top: 1rem; color:#fff; }}
h2 {{ font-size: 2.4rem; color:#fff; }}
h3 {{ font-size: 1.8rem; color:#fff; }}
h4 {{ font-size: 1.4rem; color:#ddd; }}

/* Sidebar Logo */
.sidebar-logo {{
  font-size: 4rem;
  text-align: center;
  line-height: 1;
}}

/* Upload zone style */
.stUploadDropzone {{
  border: 3px dashed #4ba3ff !important;
  background: rgba(255,255,255,0.12);
  border-radius: 1rem;
  padding: 2rem;
  transition: all .2s ease;
}}
.stUploadDropzone:hover {{
  transform: scale(1.02);
  border-color: #82c4ff !important;
}}

/* Hide default menu */
#MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# 3 · Sidebar: Interactive Controls with Prominent Logo
st.sidebar.markdown("<div class='sidebar-logo'>⚕️</div>", unsafe_allow_html=True)
st.sidebar.title("Neura Health Simulator")
st.sidebar.markdown("Use the controls below to navigate between simulations:")

condition = st.sidebar.radio(
    "Select Condition:",
    options=["Pneumonia", "Brain Tumor", "Lung Cancer"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.expander("About this App").markdown(
    "This is a demo simulation of medical image analysis. "
    "It does **not** perform real diagnostics."
)

# 4 · Map selections
titles = {
    "Pneumonia": "Pneumonia Detection",
    "Brain Tumor": "Brain Tumor Detection",
    "Lung Cancer": "Lung Cancer Detection"
}
labels = {
    "Pneumonia":    ("NORMAL LUNG", "PNEUMONIA"),
    "Brain Tumor":  ("NO TUMOR",    "TUMOR DETECTED"),
    "Lung Cancer":  ("HEALTHY LUNG", "CANCER DETECTED")
}

# 5 · Main Title & Instructions
st.title("⚕️ Neura Health Simulator")
st.markdown("---")
st.header(titles[condition])
st.markdown(
    "Upload a scan below to run a simulated analysis."
)

# 6 · File Uploader
uploaded = st.file_uploader(
    "Choose an image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

# 7 · Simulation & Display
if uploaded:
    # Show loader with spinner and progress bar
    with st.spinner("Analyzing image…"):
        progress = st.progress(0)
        for pct in range(1, 101):
            time.sleep(0.02)
            progress.progress(pct)

    # Fake score
    score = random.randint(0, 99)
    healthy_label, sick_label = labels[condition]
    result_label = healthy_label if score < 50 else sick_label
    color = "#2ecc71" if score < 50 else "#e74c3c"

    # Prepare images
    orig = Image.open(uploaded).convert("RGB")
    badge = orig.copy()
    draw = ImageDraw.Draw(badge)
    W, H = badge.size
    fs = max(W // 15, 24)
    try:
        font = ImageFont.truetype("arial.ttf", fs)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), result_label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 10
    box = [
        (W - tw) // 2 - pad,
        H - th - 3 * pad,
        (W + tw) // 2 + pad,
        H - pad
    ]
    draw.rounded_rectangle(box, fill=color + "AA", radius=th // 2)
    draw.text(
        ((W - tw) // 2, H - th - 2 * pad),
        result_label,
        fill="white",
        font=font
    )

    # Display side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Scan")
        st.image(orig, width=300)
    with col2:
        st.subheader("Simulated Result")
        st.image(badge, width=300)

    # Big result text
    st.markdown(
        f"<h2 style='text-align:center; color:{color};'>"
        f"{score}% chance of {result_label.lower()}"
        f"</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

# 8 · Footer
st.markdown(
    "<div class='footer'>Neura Health &copy; 2025</div>",
    unsafe_allow_html=True
)
