import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Dashboard Creator")

# Streamlit Deploy Link
STREAMLIT_DEPLOY_URL = "https://share.streamlit.io/deploy?repository=meetmoliya904-dev/my-stock-scanner&branch=main&mainModulePath=app.py"

# Custom Styling
st.markdown("""
<style>
    .stButton>button {
        background-color: #0080FF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .metric-card {
        border: 1px solid #2e2e2e;
        padding: 15px;
        border-radius: 10px;
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🎯 HEADER SECTION WITH "CREATE NEW DASHBOARD"
# -------------------------------------------------------------
head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    st.title("📊 Stoxify - Live Scanner Dashboard")

with head_col2:
    st.write("") # Spacing
    # ડાયરેક્ટ Streamlit ના કનેક્ટ પેજ પર મોકલતું બટન
    st.link_button("➕ Create new dashboard", STREAMLIT_DEPLOY_URL, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# 🎯 SIDEBAR PANEL
# -------------------------------------------------------------
st.sidebar.title("🛠️ Stoxify Dashboard Builder")
st.sidebar.markdown("---")

dashboard_name = st.sidebar.text_input("📌 Dashboard Name:", value="My Custom Scanner")
scan_segment = st.sidebar.selectbox("📊 Select Segment:", ["CASH (Watchlist)", "SECTORS", "ALL NSE STOCKS"])
refresh_time = st.sidebar.slider("⏱️ Auto Refresh (Seconds):", 10, 300, 60)

st.sidebar.markdown("---")
if st.sidebar.button("🚀 Deploy New Instance"):
    st.sidebar.success("Redirecting to Streamlit Deploy...")
    st.markdown(f'<meta http-equiv="refresh" content="0;url={STREAMLIT_DEPLOY_URL}">', unsafe_allow_html=True)

# -------------------------------------------------------------
# 📊 MAIN DASHBOARD WIDGETS
# -------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 1. BULLISH BREAKOUTS")
    st.info("નવા સ્કેનર માટે 'Create new dashboard' દબાવીને કનેક્ટ કરો.")

    st.markdown("---")

    st.subheader("📈 2. BULLISH SECTORS")
    st.info("લાઈવ સ્કેનિંગ શરૂ કરવા માટે રેડી.")

with col2:
    st.subheader("🔴 3. BEARISH BREAKOUTS")
    st.info("નવા સ્કેનર માટે 'Create new dashboard' દબાવીને કનેક્ટ કરો.")

    st.markdown("---")

    st.subheader("📉 4. BEARISH SECTORS")
    st.info("લાઈવ સ્કેનિંગ શરૂ કરવા માટે રેડી.")
    
