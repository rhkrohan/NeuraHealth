# pneumonia_app.py  ────────────────────────────────────────────────
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import io, base64

# ──────────────────────────────────────────────────────────────────
# 0 ·  Page setup  (same styling pattern you provided)
# ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Pneumonia Detector", page_icon="⚕️")

hide_streamlit_style = """
<style>
#MainMenu {visibility:hidden;}
footer    {visibility:hidden;}
header    {visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

background_image_url = "https://i.imgur.com/ji75q6m.jpg"   # any medical bg
bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
  background-image: url("{background_image_url}");
  background-attachment: fixed;
  background-size: cover;
  background-position: center;
}}
[data-testid="stAppViewContainer"]::before {{
   content:"";
   position:absolute;top:0;left:0;width:100%;height:100%;
   background:rgba(0,0,0,0.6);
}}
</style>
"""
st.markdown(bg_css, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# 1 ·  Load Keras model (cached)
# ──────────────────────────────────────────────────────────────────
MODEL_PATH = "/Users/rohankhan/Desktop/NeuraHealth/Models/pneumonia.h5"     # <- change if different
IMG_SIZE   = 160                        # match training size
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]

@st.cache_resource(show_spinner="Loading model …")
def get_model():
    return load_model(MODEL_PATH)

model = get_model()

# ──────────────────────────────────────────────────────────────────
# 2 ·  Pre-processing  (letter-box, 0-1 float)
# ──────────────────────────────────────────────────────────────────
def preprocess_pil(pil_img, size=IMG_SIZE):
    pil_img = pil_img.convert("RGB")
    w, h = pil_img.size
    scale = size / max(w, h)
    nw, nh = int(round(w*scale)), int(round(h*scale))
    img_rs = pil_img.resize((nw, nh), Image.BILINEAR)

    canvas = Image.new("RGB", (size, size), (0, 0, 0))
    canvas.paste(img_rs, ((size-nw)//2, (size-nh)//2))
    arr = np.asarray(canvas, dtype="float32")/255.0
    return canvas, arr

# (optional) Grad-CAM
def grad_cam(img_tensor, model, last_conv="block_15_add"):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv).output, model.output])
    with tf.GradientTape() as tape:
        conv_out, pred = grad_model(img_tensor)
        loss = pred[:,0]
    grads  = tape.gradient(loss, conv_out)
    pooled = tf.reduce_mean(grads, axis=[1,2])
    conv_out, pooled = conv_out[0], pooled[0]
    heat = tf.reduce_sum(conv_out * pooled, axis=-1)
    heat = tf.maximum(heat,0) / tf.reduce_max(heat)
    heat = np.uint8(255 * heat.numpy())
    heat = Image.fromarray(heat).resize((IMG_SIZE,IMG_SIZE))
    return np.asarray(heat)/255.0

# ──────────────────────────────────────────────────────────────────
# 3 ·  UI
# ──────────────────────────────────────────────────────────────────
st.title("⚕️ Chest-X-ray Pneumonia Detector")

uploaded = st.file_uploader("Upload a chest X-ray JPEG/PNG", type=["jpg","jpeg","png"])

if uploaded:
    pil_orig = Image.open(uploaded)
    st.subheader("Original image")
    st.image(pil_orig, use_column_width=True)

    padded_pil, arr = preprocess_pil(pil_orig)
    x = np.expand_dims(arr, 0)

    prob = float(model.predict(x, verbose=0)[0][0])
    pred = CLASS_NAMES[int(prob>=0.5)]

    st.subheader("Model input (letter-boxed)")
    st.image(padded_pil, width=300)

    st.markdown(f"### **Prediction:** {pred}")
    st.markdown(f"Probability of *pneumonia*: **{prob*100:.1f}%**")

    if st.checkbox("Show Grad-CAM heat-map"):
        heat = grad_cam(x, model)
        overlay = np.asarray(padded_pil)/255.0*0.5 + np.expand_dims(heat,2)*0.5
        st.image(overlay, caption="Red = regions influencing prediction")
