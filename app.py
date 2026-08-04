import streamlit as st
import json
import os

# Page Configuration
st.set_page_config(layout="wide", page_title="Acharya - Atlas Financial Intelligence", page_icon="📈")

# Local Storage File for Persistence
DATA_FILE = "acharya_dashboards.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return [
        {"id": 1, "name": "IBB SCANNER", "desc": "Has 4 widgets", "is_private": True, "is_fav": True, "widgets": 4}
    ]

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "dashboards" not in st.session_state:
    st.session_state.dashboards = load_data()

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home" # 'home', 'create', 'dashboard_view'

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Your"

# Custom Styling to match Image 1000223920.jpg Exactly
st.markdown("""
<style>
    /* Dark Theme Setup */
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    
    /* Top Logo & Branding Header */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0px;
        border-bottom: 1px solid #1e2640;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    .brand-badge {
        background: linear-gradient(90deg, #1d976c, #2c3e50);
        color: #00ffff;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        margin-left: 8px;
    }
    
    /* Center CI Hero Section */
    .hero-box {
        text-align: center;
        padding: 30px 10px;
    }
    .ci-logo {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 2px solid #818cf8;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        color: #818cf8;
        box-shadow: 0 0 20px rgba(129, 140, 248, 0.4);
        margin-bottom: 15px;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .hero-sub {
        font-size: 14px;
        color: #94a3b8;
        max-width: 500px;
        margin: 0 auto 20px auto;
    }
    
    /* Glowing Action Button */
    .scan-btn {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4);
        color: white;
        padding: 12px 28px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 14px;
        border: none;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
        display: inline-block;
    }
    
    /* Studio Card Outer Box */
    .studio-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 20px;
        margin-top: 25px;
    }
    
    /* Create Dashboard Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        height: 48px !important;
    }
    
    /* Card Styles */
    .card-item {
        background: #0f172a;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🔱 TOP BRANDING HEADER
# -------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div>
        <span class="brand-title">Acharya</span>
        <span class="brand-badge">SCANNER</span>
        <br><small style="color:#64748b; font-size:10px;">ATLAS FINANCIAL INTELLIGENCE</small>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. HOME VIEW (MATCHING IMAGE 1000223920.JPG)
# -------------------------------------------------------------
if st.session_state.view_mode == "home":
    
    # Hero Center Box
    st.markdown("""
    <div class="hero-box">
        <div class="ci-logo">Ci</div>
        <div class="hero-title">Finance analysis tools</div>
        <div class="hero-sub">Customizing stock charts, scans, and widgets — free and fast, so you get the insights you need to improve your trades.</div>
        <div class="scan-btn">SCAN. CHART. TRADE.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Acharya Dashboards Studio Section
    st.markdown("### <span style='background:#312e81; color:#c7d2fe; padding:3px 8px; border-radius:4px; font-size:12px;'>ATLAS</span> Acharya Dashboards Studio", unsafe_allow_html=True)
    st.caption("Customize scan result columns, view sector performance, track trends, view multiple scans in a single view.")
    
    st.write("")
    
    # Create Dashboard Button
    if st.button("+ Create Dashboard", type="primary", use_container_width=True):
        st.session_state.view_mode = "create"
        st.rerun()
        
    st.write("")
    
    # Tabs: Your | Top | Fav
    tab_col1, tab_col2, tab_col3, tab_space = st.columns([1, 1, 1, 3])
    with tab_col1:
        if st.button("Your", type="secondary" if st.session_state.active_tab == "Your" else "tertiary"):
            st.session_state.active_tab = "Your"
            st.rerun()
    with tab_col2:
        if st.button("Top"):
            st.session_state.active_tab = "Top"
            st.rerun()
    with tab_col3:
        if st.button("Fav"):
            st.session_state.active_tab = "Fav"
            st.rerun()
            
    st.markdown("---")
    
    # Filter list based on tab
    dash_list = st.session_state.dashboards
    if st.session_state.active_tab == "Fav":
        dash_list = [d for d in dash_list if d.get("is_fav", False)]
        
    if len(dash_list) == 0:
        st.info("No dashboards found in this section.")
        
    for idx, d in enumerate(dash_list):
        with st.container():
            col_info, col_actions = st.columns([3, 1])
            
            with col_info:
                if st.button(f"📌 {d['name']}", key=f"open_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.session_state.view_mode = "dashboard_view"
                    st.rerun()
                st.caption(f"Has {d.get('widgets', 0)} widgets")
                
            with col_actions:
                c1, c2, c3 = st.columns(3)
                with c1:
                    fav_icon = "⭐" if d.get("is_fav", False) else "☆"
                    if st.button(fav_icon, key=f"fav_{d['id']}"):
                        d["is_fav"] = not d.get("is_fav", False)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                with c2:
                    if st.button("📋", key=f"copy_{d['id']}"):
                        copied = json.loads(json.dumps(d))
                        copied["id"] = len(st.session_state.dashboards) + 1
                        copied["name"] = f"{d['name']} (COPY)"
                        st.session_state.dashboards.append(copied)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                with c3:
                    if st.button("🗑️", key=f"del_{d['id']}"):
                        st.session_state.dashboards.pop(idx)
                        save_data(st.session_state.dashboards)
                        st.rerun()
                        
            st.markdown("---")

# -------------------------------------------------------------
# 2. CREATE NEW DASHBOARD FORM
# -------------------------------------------------------------
elif st.session_state.view_mode == "create":
    if st.button("⬅️ Back"):
        st.session_state.view_mode = "home"
        st.rerun()
        
    st.title("🛠️ Create Dashboard")
    st.markdown("---")
    
    with st.form("create_form"):
        d_name = st.text_input("Title", placeholder="e.g. IBB SCANNER or MOJ")
        is_pvt = st.checkbox("Private Premium", value=True)
        
        st.write("")
        col_cancel, col_create = st.columns(2)
        with col_create:
            sub = st.form_submit_button("Create", type="primary", use_container_width=True)
            
        if sub:
            if d_name.strip() != "":
                new_d = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": d_name.upper(),
                    "desc": "Has 0 widgets",
                    "is_private": is_pvt,
                    "is_fav": False,
                    "widgets": 0
                }
                st.session_state.dashboards.append(new_d)
                save_data(st.session_state.dashboards)
                st.session_state.view_mode = "home"
                st.rerun()
            else:
                st.error("Please enter a title!")

# -------------------------------------------------------------
# 3. DASHBOARD DETAILS VIEW
# -------------------------------------------------------------
elif st.session_state.view_mode == "dashboard_view":
    active = st.session_state.active_dashboard
    
    if st.button("⬅️ Back"):
        st.session_state.view_mode = "home"
        st.rerun()
        
    st.title(f"📊 {active['name']}")
    st.markdown("---")
    st.info("Scanner Active! Live Market Breakout Data is fetching in real-time...")
    
