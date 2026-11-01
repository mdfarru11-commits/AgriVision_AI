
import os
import base64
import hashlib
from io import BytesIO

import requests
import streamlit as st
import plotly.graph_objects as go
from PIL import Image


# ---------------- CONFIGURATION ----------------

try:
    API_URL = st.secrets.get(
        "API_URL",
        os.getenv("API_URL", "http://127.0.0.1:8000")
    )
except Exception:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AgriVision AI | ByteSquad",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = [
    "Dashboard",
    "Crop Analysis",
    "Field Mapping",
    "Recommendations",
]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ---------------- PREMIUM THEME ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0a110e;
    --surface: #111e17;
    --surface2: #17271d;
    --border: #263d2d;
    --green: #91e6a3;
    --green2: #b8f2c3;
    --muted: #94aa9a;
    --white: #edf6ee;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #173524 0%, transparent 35%),
        var(--bg);
    color: var(--white);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0e1913;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--muted);
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--white) !important;
    letter-spacing: -0.5px;
}

h1 { font-weight: 700 !important; }
h2, h3 { font-weight: 600 !important; }

p, label, .stMarkdown {
    color: #c1d1c5;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17281e, #111e17);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 19px 20px;
    min-height: 115px;
}

[data-testid="stMetricLabel"] {
    color: #a8bdad !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: var(--green2) !important;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
}

.stButton > button {
    background: linear-gradient(110deg, #a2edaf, #78d88d);
    color: #102016;
    border: 1px solid #a2edaf;
    border-radius: 11px;
    min-height: 46px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #c0f5c8;
    color: #102016;
    border-color: #c0f5c8;
    transform: translateY(-1px);
}

.stButton > button:focus {
    box-shadow: 0 0 0 2px #0a110e, 0 0 0 4px #91e6a3;
}

[data-testid="stFileUploader"] {
    background: #14231a;
    border: 1px dashed #527e5d;
    border-radius: 15px;
    padding: 14px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stSelectbox"] > div > div {
    background: #17271d;
    border-color: var(--border);
    border-radius: 10px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: var(--border);
}

.hero {
    background:
        radial-gradient(circle at 90% 15%, #356b42 0%, transparent 28%),
        linear-gradient(120deg, #173c27, #12251a 70%, #1c3825);
    border: 1px solid #365b40;
    border-radius: 22px;
    padding: 36px;
    margin-bottom: 28px;
}

.hero-tag {
    color: #a7edb3;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.5px;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(28px, 4vw, 43px);
    font-weight: 700;
    color: #f0fff1;
    line-height: 1.15;
    margin-bottom: 13px;
}

.hero-subtitle {
    color: #c5dccb;
    font-size: 15px;
    line-height: 1.7;
    max-width: 680px;
}

.panel {
    background: linear-gradient(145deg, #17281e, #111e17);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 23px;
    min-height: 160px;
    margin-bottom: 12px;
}

.panel h3 {
    font-size: 19px;
    margin-bottom: 10px;
}

.panel p {
    color: #a9bdaf;
    font-size: 14px;
    line-height: 1.7;
}

.eyebrow {
    color: #91e6a3;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.section-note {
    color: var(--muted);
    font-size: 13px;
    margin-top: -7px;
    margin-bottom: 20px;
}

.small-muted {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    background: #193b26;
    border: 1px solid #356a42;
    color: #a9edb5;
    padding: 6px 11px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.result-card {
    background: linear-gradient(145deg, #1a3022, #122219);
    border: 1px solid #3d6547;
    border-radius: 17px;
    padding: 22px;
    margin: 10px 0 18px 0;
}

.footer {
    text-align: center;
    color: #718b78;
    font-size: 12px;
    padding: 15px 0 5px 0;
}

[data-testid="stImage"] img {
    border-radius: 14px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPERS ----------------

def api_status():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.ok
    except requests.RequestException:
        return False


def title_block(title, subtitle):
    st.markdown(f"""
    <div class="eyebrow">AGRIVISION AI WORKSPACE</div>
    <h1 style="font-size:34px;margin-bottom:5px">{title}</h1>
    <p class="section-note">{subtitle}</p>
    """, unsafe_allow_html=True)


def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()


def clean_label(value):
    return str(value).replace("_", " ").strip()


# ---------------- SIDEBAR ----------------

online = api_status()

with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 15px 0">
        <div style="font-size:27px;font-weight:800;color:#b8f2c3;
                    font-family:Outfit,sans-serif">
            🌱 AgriVision AI
        </div>
        <div style="font-size:10px;letter-spacing:2px;
                    color:#8ca995;font-weight:700">
            INTELLIGENT AGRICULTURE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="eyebrow">MAIN MENU</div>',
        unsafe_allow_html=True
    )

    st.selectbox(
        "Navigate",
        PAGES,
        key="page",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="eyebrow">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    if online:
        st.success("● AI Engine Online")
    else:
        st.error("● AI Engine Offline")

    st.caption("ONNX · FastAPI · Image Classification")

    st.divider()

    st.markdown("""
    <div style="background:#17271d;border:1px solid #294333;
                border-radius:13px;padding:15px">
        <div style="color:#a9edb5;font-size:12px;font-weight:800">
            BUILT BY
        </div>
        <div style="color:#edf6ee;font-size:17px;font-weight:700;
                    margin-top:4px">ByteSquad</div>
        <div style="color:#91a99a;font-size:11px;margin-top:4px">
            AI Manthan 2.0
        </div>
    </div>
    """, unsafe_allow_html=True)


page = st.session_state.page


# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ AGRICULTURAL INTELLIGENCE PLATFORM</div>
        <div class="hero-title">
            Smarter farming.<br>Healthier crops.
        </div>
        <div class="hero-subtitle">
            Analyze crop images with AI, understand potential health
            conditions and explore how precision agriculture can
            support smarter field-level decisions.
        </div>
        <div style="margin-top:22px">
            <span class="status-pill">AI-POWERED CROP MONITORING</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    title_block(
        "Platform Overview",
        "Your crop intelligence workspace at a glance."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("AI Engine", "Online" if online else "Offline")
    c2.metric("Supported Classes", "38")
    c3.metric("Inference Engine", "ONNX")
    c4.metric("Processing", "Local API")

    st.markdown("### Explore the platform")
    st.markdown(
        '<p class="section-note">Tools designed to make crop monitoring easier.</p>',
        unsafe_allow_html=True
    )

    a, b = st.columns(2, gap="large")

    with a:
        st.markdown("""
        <div class="panel">
            <div class="eyebrow">01 · IMAGE INTELLIGENCE</div>
            <h3>🌿 Crop Health Analysis</h3>
            <p>
                Upload a crop leaf photograph and get an AI-generated
                classification, confidence score and alternative predictions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Crop Analysis →", use_container_width=True):
            go_to("Crop Analysis")

    with b:
        st.markdown("""
        <div class="panel">
            <div class="eyebrow">02 · SPATIAL VISUALIZATION</div>
            <h3>🗺️ Field Health Mapping</h3>
            <p>
                Explore an illustrative field-zone heatmap and understand
                how localized crop monitoring can support intervention planning.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore Field Mapping →", use_container_width=True):
            go_to("Field Mapping")

    st.markdown("### How AgriVision AI works")

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("""
        <div class="panel">
            <div class="eyebrow">STEP 01</div>
            <h3>📷 Capture</h3>
            <p>Upload a clear crop or leaf photograph for analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="panel">
            <div class="eyebrow">STEP 02</div>
            <h3>🧠 Analyze</h3>
            <p>The ONNX image classifier evaluates the uploaded image.</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="panel">
            <div class="eyebrow">STEP 03</div>
            <h3>🎯 Review</h3>
            <p>Review predictions and general crop-monitoring guidance.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Prototype note: The classifier uses PlantVillage categories. "
        "Dashboard metrics and field zones are illustrative, not live farm "
        "measurements. Model predictions are not confirmed diagnoses."
    )


# =====================================================
# CROP ANALYSIS
# =====================================================

elif page == "Crop Analysis":

    title_block(
        "Crop Health Analysis",
        "Upload a leaf photograph and let the ONNX model analyze it."
    )

    st.markdown("""
    <div class="panel">
        <div class="eyebrow">AI IMAGE CLASSIFICATION</div>
        <h3>Upload your crop image</h3>
        <p>
            For a useful result, choose a clear, well-lit image with
            the leaf visible and in focus.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choose a crop or leaf photograph",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG and PNG."
    )

    if uploaded:
        image_bytes = uploaded.getvalue()
        image_hash = hashlib.sha256(image_bytes).hexdigest()

        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")

            left, right = st.columns([1, 1.15], gap="large")

            with left:
                st.image(
                    image,
                    caption="Uploaded crop photograph",
                    use_container_width=True
                )

            with right:
                st.markdown("### Image information")

                st.markdown(f"""
                <div class="panel">
                    <p><b>Filename</b><br>{uploaded.name}</p>
                    <p><b>Image dimensions</b><br>{image.width} × {image.height}</p>
                    <p><b>File size</b><br>{len(image_bytes) / 1024:.1f} KB</p>
                    <p><b>Format</b><br>RGB image</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "🔍  Analyze Crop Health",
                    use_container_width=True
                ):
                    if not online:
                        st.error(
                            "AI backend is offline. Start the FastAPI server first."
                        )
                    else:
                        with st.spinner(
                            "Analyzing image with the AI model..."
                        ):
                            try:
                                payload = {
                                    "file_name": uploaded.name,
                                    "image_base64": base64.b64encode(
                                        image_bytes
                                    ).decode("utf-8"),
                                }

                                response = requests.post(
                                    f"{API_URL}/analyze",
                                    json=payload,
                                    timeout=90,
                                )

                                if response.ok:
                                    st.session_state.last_result = response.json()
                                    st.session_state.last_result_hash = image_hash
                                    st.success("Image analysis completed.")
                                else:
                                    st.error(
                                        f"Analysis failed: {response.text[:500]}"
                                    )

                            except requests.RequestException as error:
                                st.error(f"Backend connection error: {error}")

            result = st.session_state.get("last_result")
            result_hash = st.session_state.get("last_result_hash")

            if result and result_hash == image_hash:
                st.divider()

                st.markdown("### Analysis Results")
                st.markdown(
                    '<span class="status-pill">ONNX MODEL PREDICTION</span>',
                    unsafe_allow_html=True
                )

                predictions = result.get("predictions", [])

                if predictions:
                    prediction = predictions[0]

                    crop = clean_label(prediction["crop"])
                    condition = clean_label(prediction["condition"])
                    confidence = float(prediction["confidence"])

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="eyebrow">PRIMARY PREDICTION</div>
                        <h2 style="margin-bottom:7px">{crop}</h2>
                        <div style="font-size:18px;color:#b8f2c3;
                                    font-weight:700">{condition}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    r1, r2, r3 = st.columns(3)
                    r1.metric("Detected Crop", crop)
                    r2.metric("Predicted Condition", condition)
                    r3.metric("Model Confidence", f"{confidence:.2f}%")

                    st.markdown("### Prediction distribution")

                    for index, item in enumerate(predictions, start=1):
                        label = (
                            f"{clean_label(item['crop'])} — "
                            f"{clean_label(item['condition'])}"
                        )
                        score = float(item["confidence"])

                        st.markdown(f"**{index}. {label}**")
                        st.progress(min(1.0, max(0.0, score / 100)))
                        st.caption(f"Model confidence: {score:.2f}%")

                    if "healthy" in condition.lower():
                        st.success(
                            "The model classified this image as healthy. "
                            "Continue routine monitoring and verify the "
                            "crop's condition in the field."
                        )
                    else:
                        st.warning(
                            "The model identified a possible crop-health "
                            "condition. Inspect the plant and seek confirmation "
                            "from a qualified agricultural expert."
                        )

                    if result.get("notice"):
                        st.caption(result["notice"])

                    st.caption(
                        "Confidence is the model's classification score. "
                        "It does not establish diagnostic certainty."
                    )

                else:
                    st.warning("No prediction data was returned by the model.")

        except Exception as error:
            st.error(f"Unable to read this image: {error}")

    else:
        st.info("Upload a clear leaf photograph to begin AI analysis.")


# =====================================================
# FIELD MAPPING
# =====================================================

elif page == "Field Mapping":

    title_block(
        "Field Health Mapping",
        "Explore how crop monitoring can be represented across field zones."
    )

    st.warning(
        "DEMO VISUALIZATION: The values below are illustrative. "
        "They are not real GPS coordinates or AI-derived field measurements."
    )

    z1, z2, z3 = st.columns(3)
    z1.metric("Illustrative Zones", "9")
    z2.metric("Visualization", "3 × 3 Grid")
    z3.metric("Map Status", "Demo")

    st.markdown("### Field zone overview")
    st.markdown(
        '<p class="section-note">Illustrative crop-health scores across nine zones.</p>',
        unsafe_allow_html=True
    )

    values = [
        [92, 85, 78],
        [88, 58, 72],
        [95, 67, 90],
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=values,
            x=["Zone A", "Zone B", "Zone C"],
            y=["North", "Middle", "South"],
            zmin=0,
            zmax=100,
            colorscale=[
                [0.0, "#b94f4f"],
                [0.5, "#d6ad50"],
                [1.0, "#62b77a"],
            ],
            colorbar=dict(
                title=dict(text="Illustrative score")
            ),
            text=[[f"{value}%" for value in row] for row in values],
            texttemplate="%{text}",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Score: %{z}%"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        paper_bgcolor="#111e17",
        plot_bgcolor="#111e17",
        font=dict(color="#e8f3e9", family="DM Sans"),
        height=440,
        margin=dict(l=20, r=20, t=25, b=20),
        xaxis=dict(side="top"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Understanding the zones")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="panel">
            <h3 style="color:#b9e7c2">🟢 Higher score</h3>
            <p>Illustrative zones with higher displayed health scores.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="panel">
            <h3 style="color:#e8cb83">🟡 Moderate score</h3>
            <p>Illustrative zones that may require closer observation.</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="panel">
            <h3 style="color:#edaaaa">🔴 Lower score</h3>
            <p>Illustrative zones shown for monitoring demonstration.</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "Future integration: geotagged field images, real field boundaries "
        "and location-specific AI analysis."
    )


# =====================================================
# RECOMMENDATIONS
# =====================================================

elif page == "Recommendations":

    title_block(
        "Agricultural Recommendations",
        "General monitoring guidance based on your latest model prediction."
    )

    result = st.session_state.get("last_result")

    if not result:
        st.info(
            "No analysis is available yet. Analyze a crop image first "
            "to see related guidance."
        )

        if st.button("Go to Crop Analysis →", use_container_width=True):
            go_to("Crop Analysis")

    else:
        predictions = result.get("predictions", [])

        if predictions:
            prediction = predictions[0]
            crop = clean_label(prediction["crop"])
            condition = clean_label(prediction["condition"])
            confidence = float(prediction["confidence"])

            st.markdown(f"""
            <div class="result-card">
                <div class="eyebrow">LATEST MODEL PREDICTION</div>
                <h2>{crop}</h2>
                <p style="color:#b8f2c3;font-size:18px;
                          font-weight:700">{condition}</p>
                <p>Model confidence: {confidence:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

            if "healthy" in condition.lower():
                st.success(
                    "The model classified the uploaded image as healthy. "
                    "Continue regular monitoring and maintain appropriate "
                    "field hygiene."
                )
            else:
                st.warning(
                    "A possible crop-health issue was identified. "
                    "Inspect nearby plants, record affected locations "
                    "and consult a local agricultural expert."
                )

            st.markdown("### Suggested monitoring steps")

            st.markdown("""
            1. Capture additional clear photographs of affected plants.
            2. Compare visible symptoms across different parts of the field.
            3. Record the affected field zone and date.
            4. Consult a qualified agricultural expert before selecting treatment.
            """)

            st.caption(
                "AI predictions are advisory estimates, not confirmed "
                "diagnoses or treatment prescriptions."
            )

            if st.button("Analyze another image", use_container_width=True):
                go_to("Crop Analysis")


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div class="footer">
    <b style="color:#a9edb5">🌱 AgriVision AI</b><br>
    Built with innovation by ByteSquad · AI Manthan 2.0<br>
    <span style="font-size:11px">AI-powered crop monitoring prototype</span>
</div>
""", unsafe_allow_html=True)
