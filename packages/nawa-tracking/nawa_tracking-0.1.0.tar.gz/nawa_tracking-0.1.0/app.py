import time, tempfile, pandas as pd
from pathlib import Path
import streamlit as st
import plotly.express as px
from nawa.matcher import real_match
from nawa.report import build_pdf   # adjust if your report fn name differs

st.set_page_config(page_title="NAWA Face‎Match Dashboard",
                   page_icon="🕋", layout="centered")

# ── Sidebar ───────────────────────────────
st.sidebar.title("Settings")
collection = st.sidebar.text_input("AWS Collection ID", "NAWA_PILGRIMS")
threshold  = st.sidebar.slider("Match threshold (%)", 70, 100, 90)

st.sidebar.markdown("---")
if st.sidebar.button("Clear session log"):
    st.session_state["log"] = []

# ── Main UI ──────────────────────────────
st.title("🧐 NAWA Realtime Face Matcher")

uploaded = st.file_uploader("Upload a JPG/PNG face", type=["jpg", "jpeg", "png"])
cam_shot = st.camera_input("...or capture via webcam")

image_bytes = None
if uploaded:
    image_bytes = uploaded.getvalue()
elif cam_shot:
    image_bytes = cam_shot.getvalue()

if image_bytes:
    t0 = time.time()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    res = real_match(tmp_path, collection_id=collection, threshold=threshold)
    latency = round(time.time() - t0, 3)
    res["latency_ms"] = latency * 1000

    # Render result
    st.success(f"**Match:** `{res['name'] or 'Unknown'}`  \n"
               f"**Confidence:** {res['confidence']}\u202f%  \n"
               f"**Latency:** {res['latency_ms']:.0f} ms")

    # Save log in session_state
    st.session_state.setdefault("log", []).append(res)

    # PDF button
    if st.button("Generate PDF report"):
        pdf_path = build_pdf(res)     # implement build_pdf → returns filename
        st.download_button("Download PDF", open(pdf_path, "rb"), file_name="nawa_report.pdf")

# ── Log table & simple chart ────────────────────────
log_df = pd.DataFrame(st.session_state.get("log", []))

if not log_df.empty and "latency_ms" in log_df.columns:
    import plotly.express as px

    st.subheader("Recent matches")
    st.dataframe(log_df)

    fig = px.line(log_df.tail(20), y="latency_ms", title="Latency (ms)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No latency data available to plot yet.")

# EOF ──────────────────────────────

