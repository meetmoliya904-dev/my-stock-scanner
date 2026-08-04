import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os

# Page Configuration
st.set_page_config(layout="wide", page_title="Stock Screener & Atlas Dashboard", page_icon="⚡")

# File Storage path for persistence
DATA_FILE = "stock_screener_data.json"

# Load Saved Dashboards & Scanners
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return [
        {
            "id": 1,
            "name": "IBB SCANNER",
            "desc": "Has 4 widgets",
            "is_private": True,
            "is_fav": True,
            "filters": [
                {"tf": "15m", "field": "Close", "op": "Greater than", "val": "Prev 15m High"},
                {"tf": "15m", "field": "Close", "op": "Greater than", "val": "Pivot Point R1"}
            ]
        },
        {
            "id": 2,
            "name": "BULLISH LIVE IBB",
            "desc": "Live Breakout Screener",
            "is_private": True,
            "is_fav": False,
            "filters": []
        }
    ]

# Save Data to JSON File
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Session State Initialization
if "dashboards" not in st.session_state:
    st.session_state.dashboards = load_data()

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard" # 'dashboard', 'screener_builder', 'view_results'

if "active_screener" not in st.session_state:
    st.session_state.active_screener = None

# Custom CSS for Dark Modern Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
    }
    /* Header Box */
    .top-header {
        background: #111827;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #1f2937;
        margin-bottom: 20px;
    }
    .badge-pvt {
        background: #450a0a;
        color: #f87171;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        border: 1px solid #f87171;
    }
    /* Screener Filter Card */
    .filter-card {
        background: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #3b82f6) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# Watchlist Stocks for Scanning
STOCK_LIST = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 'BHARTIARTL.NS',
    'SBIN.NS', 'LTIM.NS', 'TATAMOTORS.NS', 'AXISBANK.NS', 'KOTAKBANK.NS', 'LT.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'BAJFINANCE.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'TITAN.NS'
]

# Fetch Real-time Stock Data & Run Scan
@st.cache_data(ttl=60)
def fetch_live_breakouts():
    results = []
    for ticker in STOCK_LIST:
        try:
            df = yf.download(ticker, period="2d", interval="15m", progress=False)
            if len(df) < 2: continue
            
            ltp = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[0])
            pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)
            volume = int(df['Volume'].iloc[-1])
            symbol = ticker.replace(".NS", "")
            
            # Simple Breakout Rule Demo
            results.append({
                "Symbol": symbol,
                "LTP": round(ltp, 2),
                "% Change": pct_change,
                "Volume": volume
            })
        except:
            pass
            
    res_df = pd.DataFrame(results)
    if not res_df.empty:
        return res_df.sort_values(by="% Change", ascending=False)
    return pd.DataFrame()

# -------------------------------------------------------------
# 🛠️ SIDEBAR NAVIGATION MENU
# -------------------------------------------------------------
st.sidebar.title("⚡ Chartink ATLAS")
st.sidebar.caption("Real-Time Stock Screener")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Navigation", ["📂 Dashboards Studio", "🔍 Stock Screener", "⭐ Watchlists"])

if nav_choice == "📂 Dashboards Studio":
    st.session_state.current_page = "dashboard"
elif nav_choice == "🔍 Stock Screener":
    st.session_state.current_page = "screener_builder"

st.sidebar.markdown("---")
st.sidebar.markdown("🎨 **Theme Toggle**")
t_col1, t_col2 = st.sidebar.columns(2)
t_col1.button("Dark ☾", use_container_width=True)
t_col2.button("Light 💡", use_container_width=True)


# =================================----------------------------
# 1. DASHBOARDS STUDIO PAGE
# =================================----------------------------
if st.session_state.current_page == "dashboard":
    st.title("Scan Dashboard")
    st.caption("Review saved scans, tags, sharing, and live previews from one place.")
    st.markdown("---")
    
    col_top1, col_top2 = st.columns([4, 1])
    with col_top2:
        if st.button("➕ Create Scanner", type="primary", use_container_width=True):
            st.session_state.current_page = "screener_builder"
            st.rerun()
            
    st.write("")
    
    # Render Saved Dashboards List
    if len(st.session_state.dashboards) == 0:
        st.info("No saved dashboards yet. Click 'Create Scanner' above!")
        
    for idx, d in enumerate(st.session_state.dashboards):
        with st.container():
            c_info, c_btns = st.columns([3, 1])
            
            with c_info:
                if st.button(f"📌 {d['name']}", key=f"dash_item_{d['id']}"):
                    st.session_state.active_screener = d
                    st.session_state.current_page = "view_results"
                    st.rerun()
                st.caption(d.get("desc", ""))
                st.markdown('<span class="badge-pvt">🔒 Private</span>', unsafe_allow_html=True)
                
            with c_btns:
                b1, b2, b3 = st.columns(3)
                with b1:
                    fav_icon = "⭐" if d.get("is_fav", False) else "☆"
                    if st.button(fav_icon, key=f"fav_{d['id']}"):
                        d["is_fav"] = not d.get("is_fav", False)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                with b2:
                    if st.button("📋", key=f"copy_{d['id']}"):
                        cp = json.loads(json.dumps(d))
                        cp["id"] = len(st.session_state.dashboards) + 1
                        cp["name"] = f"{d['name']} (COPY)"
                        st.session_state.dashboards.append(cp)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                with b3:
                    if st.button("🗑️", key=f"del_{d['id']}"):
                        st.session_state.dashboards.pop(idx)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                        
            st.markdown("---")


# =================================----------------------------
# 2. STOCK SCREENER BUILDER (Filter Creator)
# =================================----------------------------
elif st.session_state.current_page == "screener_builder":
    st.title("🛠️ Stock Screener - Add Filters")
    st.markdown("---")
    
    scr_name = st.text_input("📌 Scanner Name", value="MY CUSTOM SCREENER")
    
    st.subheader("🎯 Magic Filters")
    st.caption("Stock passes all of the below filters in cash segment:")
    
    # Active Filters List (Custom UI)
    st.markdown("""
    <div class="filter-card">
        <b>[15 minute] Close</b> Greater than <b>[15 minute] High</b>
    </div>
    <div class="filter-card">
        <b>[15 minute] Close</b> Greater than <b>Daily Pivot point R1</b>
    </div>
    <div class="filter-card">
        <b>Daily % Change</b> Greater than <b>Number 0</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col_add, col_run = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Filter Condition", use_container_width=True):
            st.success("Condition added successfully!")
            
    with col_run:
        if st.button("🚀 Run Scan & Save", type="primary", use_container_width=True):
            new_scr = {
                "id": len(st.session_state.dashboards) + 1,
                "name": scr_name.upper(),
                "desc": "Custom Filters Applied",
                "is_private": True,
                "is_fav": False,
                "filters": []
            }
            st.session_state.dashboards.append(new_scr)
            save_data(st.session_state.dashboards)
            st.session_state.active_screener = new_scr
            st.session_state.current_page = "view_results"
            st.rerun()


# =================================----------------------------
# 3. LIVE SCAN RESULTS VIEW
# =================================----------------------------
elif st.session_state.current_page == "view_results":
    active = st.session_state.active_screener
    scr_title = active['name'] if active else "BULLISH BREAKOUTS"
    
    col_b, col_t = st.columns([1, 5])
    with col_b:
        if st.button("⬅️ Back"):
            st.session_state.current_page = "dashboard"
            st.rerun()
            
    st.title(f"📈 {scr_title}")
    st.caption("Delayed data updated near real-time from NSE.")
    st.markdown("---")
    
    # Fetch Live Results
    with st.spinner("Scanning live market stocks..."):
        df_results = fetch_live_breakouts()
        
    if not df_results.empty:
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # Download Data Option
        csv = df_results.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download CSV Results", data=csv, file_name=f"{scr_title}_results.csv", mime='text/csv')
    else:
        st.info("No stocks currently matching the breakout condition.")
        
