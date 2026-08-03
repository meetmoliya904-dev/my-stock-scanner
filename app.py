import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Atlas Dashboard")

# Session State Initialization
if "dashboards" not in st.session_state:
    st.session_state.dashboards = [
        {"id": 1, "name": "TOMATO", "desc": "Custom Atlas Dashboard", "is_private": True, "is_fav": False, "widgets": []}
    ]

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "saved_list"  # Modes: 'create', 'saved_list', 'dashboard_view', 'scan_options'

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

# Custom CSS for Chartink Atlas Style Modal/Options Page
st.markdown("""
<style>
    .stButton>button {
        background-color: #0080FF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .badge-private {
        background-color: #3d1214;
        color: #ff6b6b;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 13px;
        border: 1px solid #ff6b6b;
        display: inline-block;
    }
    .badge-public {
        background-color: #123d24;
        color: #51cf66;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 13px;
        border: 1px solid #51cf66;
        display: inline-block;
    }
    /* Template Box CSS */
    .afresh-box {
        background-color: #E8F0FE;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #B6D0FE;
        margin-bottom: 20px;
    }
    .template-box {
        background-color: #E6F4EA;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #CEEAD6;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. CREATE DASHBOARD FORM
# -------------------------------------------------------------
if st.session_state.view_mode == "create":
    st.title("🛠️ Create New Dashboard")
    st.write("Enter details to create your scanner dashboard.")
    st.markdown("---")
    
    with st.form("create_dash_form"):
        dash_name = st.text_input("📌 Scanner Name", placeholder="Enter scanner name (e.g. TOMATO)")
        dash_desc = st.text_area("📝 Description (Optional)", placeholder="Write description...")
        is_pvt = st.checkbox("🔒 Make Private", value=True)
        
        st.write("")
        submit_btn = st.form_submit_button("🚀 Save / Create Dashboard", use_container_width=True)

        if submit_btn:
            if dash_name.strip() != "":
                new_dash = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": dash_name.upper(),
                    "desc": dash_desc,
                    "is_private": is_pvt,
                    "is_fav": False,
                    "widgets": []
                }
                st.session_state.dashboards.append(new_dash)
                st.session_state.active_dashboard = new_dash
                st.session_state.view_mode = "saved_list"
                st.rerun()
            else:
                st.error("Please enter a Scanner Name!")

# -------------------------------------------------------------
# 2. SAVED DASHBOARDS LIST PAGE
# -------------------------------------------------------------
elif st.session_state.view_mode == "saved_list":
    st.title("📋 Saved Dashboards")
    
    col_top1, col_top2 = st.columns([4, 1])
    with col_top2:
        if st.button("➕ Create New"):
            st.session_state.view_mode = "create"
            st.rerun()
            
    st.markdown("---")
    
    for idx, d in enumerate(st.session_state.dashboards):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Name Tab Click -> Opens Dashboard View
                if st.button(f"📌 {d['name']}", key=f"open_dash_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.session_state.view_mode = "dashboard_view"
                    st.rerun()
                
                if d['is_private']:
                    st.markdown('<span class="badge-private">🔒 Private</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-public">🌐 Public</span>', unsafe_allow_html=True)
                
                if d['desc']:
                    st.caption(d['desc'])
            
            with col2:
                c1, c2, c3 = st.columns(3)
                with c1:
                    fav_icon = "⭐" if d['is_fav'] else "☆"
                    if st.button(fav_icon, key=f"fav_{d['id']}"):
                        d['is_fav'] = not d['is_fav']
                        st.rerun()
                with c2:
                    if st.button("📋", key=f"copy_{d['id']}"):
                        copied = d.copy()
                        copied['id'] = len(st.session_state.dashboards) + 1
                        copied['name'] = f"{d['name']} (Copy)"
                        st.session_state.dashboards.append(copied)
                        st.rerun()
                with c3:
                    if st.button("🗑️", key=f"del_{d['id']}"):
                        st.session_state.dashboards.pop(idx)
                        if len(st.session_state.dashboards) == 0:
                            st.session_state.view_mode = "create"
                        st.rerun()
            
            st.markdown("---")

# -------------------------------------------------------------
# 3. DASHBOARD VIEW PAGE (Page 3 with Center Plus '+')
# -------------------------------------------------------------
elif st.session_state.view_mode == "dashboard_view":
    active = st.session_state.active_dashboard
    
    col_b, col_h = st.columns([1, 5])
    with col_b:
        if st.button("⬅️ Back"):
            st.session_state.view_mode = "saved_list"
            st.rerun()
            
    st.title(f"📊 {active['name']}")
    st.markdown("---")
    
    # If no widgets added yet, show Center Plus (+) Button
    if len(active['widgets']) == 0:
        st.write("<br><br>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([2, 1, 2])
        with col_p2:
            st.write("#### Add New Scan")
            if st.button("➕", type="primary", use_container_width=True):
                st.session_state.view_mode = "scan_options"
                st.rerun()
    else:
        # Show Widgets / Tables Added
        for w in active['widgets']:
            st.subheader(f"📈 {w['name']}")
            st.info(f"Loaded Template: {w['type']} | Live Data Fetching...")
            st.markdown("---")
            
        if st.button("➕ Add Another Widget"):
            st.session_state.view_mode = "scan_options"
            st.rerun()

# -------------------------------------------------------------
# 4. CHARTINK ATLAS SCAN OPTIONS PAGE (Page 4 - Image Options)
# -------------------------------------------------------------
elif st.session_state.view_mode == "scan_options":
    active = st.session_state.active_dashboard
    
    col_cancel, col_head = st.columns([1, 5])
    with col_cancel:
        if st.button("❌ Close"):
            st.session_state.view_mode = "dashboard_view"
            st.rerun()
            
    st.markdown("<h2 style='text-align: center;'>Create a new scan/chart</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # SECTION A: START AFRESH
    st.markdown("""
        <div class="afresh-box">
            <h3 style="color: #1A73E8; margin:0;">Start afresh</h3>
            <p style="color: #5F6368;">Create a new scan from scratch</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⟇ ➕ New Scan", use_container_width=True):
        active['widgets'].append({"name": "Custom New Scan", "type": "Custom Scratch"})
        st.session_state.view_mode = "dashboard_view"
        st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # SECTION B: START FROM A TEMPLATE (11 Options)
    st.markdown("""
        <div class="template-box">
            <h3 style="color: #137333; margin:0;">Start from a template</h3>
            <p style="color: #5F6368;">Templates can be used as a starting point for your scans, charts or tables</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")

    # List of Templates matching Image
    templates = [
        ("📈 Sector Advances %", "Sector Advances"),
        ("📊 Stocks near 52 week high", "52W High"),
        ("⚡ Top gainers %", "Top Gainers"),
        ("🌐 Industry Stocks at 52-wk high", "Industry 52W High"),
        ("📉 Average marketcap RSI", "Marketcap RSI"),
        ("📈 Marketcap Advances %", "Marketcap Advances"),
        ("📊 RSI distribution", "RSI Distribution"),
        ("📌 Stocks above VWAP", "Above VWAP"),
        ("📈 Todays Volume vs 50 SMA volume", "Volume vs 50 SMA"),
        ("💰 Positive vs Negative volumes (in lacs)", "Pos vs Neg Volume"),
        ("📑 Key financial Ratios", "Financial Ratios"),
        ("📊 YoY Sales & profits", "YoY Sales & Profit")
    ]

    # Render Template Buttons
    for temp_label, temp_code in templates:
        col_t1, col_t2 = st.columns([5, 1])
        with col_t1:
            if st.button(temp_label, key=f"btn_{temp_code}", use_container_width=True):
                active['widgets'].append({"name": temp_label, "type": temp_code})
                st.session_state.view_mode = "dashboard_view"
                st.rerun()
        with col_t2:
            st.caption("ℹ️ Info")
            
