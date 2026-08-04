import streamlit as st
import json
import os

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Chartink Atlas")

# File path to save dashboards permanently across page refreshes
DATA_FILE = "dashboards_data.json"

# Load saved dashboards from JSON file on app startup
def load_dashboards():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# Save dashboards to JSON file
def save_dashboards(dashboards):
    with open(DATA_FILE, "w") as f:
        json.dump(dashboards, f, indent=4)

# Initialize Session State
if "dashboards" not in st.session_state:
    st.session_state.dashboards = load_dashboards()

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "create" if len(st.session_state.dashboards) == 0 else "saved_list"

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

# Custom CSS for Mobile Responsive Buttons & Persistence
st.markdown("""
<style>
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 4px !important;
    }
    div[data-testid="column"] {
        width: auto !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }
    .stButton>button {
        width: 100% !important;
        border-radius: 6px !important;
        padding: 4px 4px !important;
        font-weight: bold !important;
    }
    .badge-private {
        background-color: #3d1214;
        color: #ff6b6b;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        border: 1px solid #ff6b6b;
        display: inline-block;
    }
    .badge-public {
        background-color: #123d24;
        color: #51cf66;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        border: 1px solid #51cf66;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. CREATE NEW DASHBOARD PAGE
# -------------------------------------------------------------
if st.session_state.view_mode == "create":
    st.title("🛠️ Create New Dashboard")
    st.write("Enter details to create your scanner dashboard.")
    st.markdown("---")
    
    with st.form("create_dash_form"):
        dash_name = st.text_input("📌 Scanner Name", placeholder="Enter scanner name (e.g. MOJ)")
        dash_desc = st.text_area("📝 Description (Optional)", placeholder="Write description...")
        is_pvt = st.checkbox("🔒 Make Private", value=True)
        
        st.write("")
        submit_btn = st.form_submit_button("🚀 Save / Create Dashboard", use_container_width=True)

        if submit_btn:
            if dash_name.strip() != "":
                new_dash = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": dash_name.upper(),
                    "desc": dash_desc if dash_desc else "Custom Atlas Dashboard",
                    "is_private": is_pvt,
                    "is_fav": False,
                    "widgets": []
                }
                st.session_state.dashboards.append(new_dash)
                save_dashboards(st.session_state.dashboards)  # Permanently Save Data
                st.session_state.active_dashboard = new_dash
                st.session_state.view_mode = "saved_list"
                st.rerun()
            else:
                st.error("Please enter a Scanner Name!")

# -------------------------------------------------------------
# 2. SAVED DASHBOARDS LIST PAGE (Fixed Refresh & Delete Button)
# -------------------------------------------------------------
elif st.session_state.view_mode == "saved_list":
    st.title("📋 Saved Dashboards")
    
    if st.button("➕ Create New Dashboard", type="primary", use_container_width=True):
        st.session_state.view_mode = "create"
        st.rerun()
            
    st.markdown("---")
    
    if len(st.session_state.dashboards) == 0:
        st.info("No dashboards created yet! Click 'Create New Dashboard' above to start.")
    
    for idx, d in enumerate(st.session_state.dashboards):
        with st.container():
            # Header Row
            col_name, col_badge = st.columns([3, 1])
            with col_name:
                if st.button(f"📌 {d['name']}", key=f"open_dash_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.session_state.view_mode = "dashboard_view"
                    st.rerun()
            with col_badge:
                if d.get('is_private', True):
                    st.markdown('<span class="badge-private">🔒 Private</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-public">🌐 Public</span>', unsafe_allow_html=True)
            
            st.caption(d.get('desc', ''))
            
            # Action Buttons Row: Star, Copy, Delete All Visible Side-by-Side
            col_fav, col_copy, col_del, col_space = st.columns([1, 1, 1, 3])
            
            with col_fav:
                fav_icon = "⭐" if d.get('is_fav', False) else "☆"
                if st.button(fav_icon, key=f"fav_{d['id']}"):
                    d['is_fav'] = not d.get('is_fav', False)
                    save_dashboards(st.session_state.dashboards)
                    st.rerun()
                    
            with col_copy:
                if st.button("📋", key=f"copy_{d['id']}"):
                    copied = json.loads(json.dumps(d))
                    copied['id'] = len(st.session_state.dashboards) + 1
                    copied['name'] = f"{d['name']} (COPY)"
                    st.session_state.dashboards.append(copied)
                    save_dashboards(st.session_state.dashboards)
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️", key=f"del_{d['id']}"):
                    st.session_state.dashboards.pop(idx)
                    save_dashboards(st.session_state.dashboards)  # Permanently Save Deletion
                    if len(st.session_state.dashboards) == 0:
                        st.session_state.view_mode = "create"
                    st.rerun()
            
            st.markdown("---")

# -------------------------------------------------------------
# 3. DASHBOARD VIEW PAGE
# -------------------------------------------------------------
elif st.session_state.view_mode == "dashboard_view":
    active = st.session_state.active_dashboard
    
    if st.button("⬅️ Back to Saved List"):
        st.session_state.view_mode = "saved_list"
        st.rerun()
            
    st.title(f"📊 {active['name']}")
    st.markdown("---")
    
    if len(active.get('widgets', [])) == 0:
        st.write("<br><br>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
        with col_p2:
            st.markdown("<h4 style='text-align: center;'>Add New Scan</h4>", unsafe_allow_html=True)
            if st.button("➕", type="primary", use_container_width=True):
                st.session_state.view_mode = "scan_options"
                st.rerun()
    else:
        for w in active['widgets']:
            st.subheader(f"📈 {w['name']}")
            st.info(f"Loaded Template: {w['type']} | Live Data Fetching...")
            st.markdown("---")
            
        if st.button("➕ Add Another Widget"):
            st.session_state.view_mode = "scan_options"
            st.rerun()

# -------------------------------------------------------------
# 4. CHARTINK ATLAS SCAN OPTIONS PAGE
# -------------------------------------------------------------
elif st.session_state.view_mode == "scan_options":
    active = st.session_state.active_dashboard
    
    if st.button("❌ Close"):
        st.session_state.view_mode = "dashboard_view"
        st.rerun()
            
    st.markdown("<h2 style='text-align: center;'>Create a new scan/chart</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("⟇ ➕ New Scan (Start Afresh)", use_container_width=True):
        active['widgets'].append({"name": "Custom New Scan", "type": "Custom Scratch"})
        save_dashboards(st.session_state.dashboards)
        st.session_state.view_mode = "dashboard_view"
        st.rerun()

    st.write("<br>", unsafe_allow_html=True)
    st.subheader("Start from a template")

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

    for temp_label, temp_code in templates:
        if st.button(temp_label, key=f"btn_{temp_code}", use_container_width=True):
            active['widgets'].append({"name": temp_label, "type": temp_code})
            save_dashboards(st.session_state.dashboards)
            st.session_state.view_mode = "dashboard_view"
            st.rerun()
                
