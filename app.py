import streamlit as st
import json
import os

# Page Configuration
st.set_page_config(layout="wide", page_title="Acharya - Atlas Financial Intelligence", page_icon="📈")

# JSON Storage File path
DATA_FILE = "acharya_atlas_data.json"

# Load saved dashboards from persistent JSON
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return [
        {"id": 1, "name": "IBB SCANNER", "desc": "Has 4 widgets", "is_private": True, "is_fav": True, "widgets": []},
        {"id": 2, "name": "TOMATO", "desc": "Has 0 widgets", "is_private": True, "is_fav": False, "widgets": []}
    ]

# Save dashboards to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize Session States
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "dashboards" not in st.session_state:
    st.session_state.dashboards = load_data()

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home" # 'home', 'create_dashboard', 'view_dashboard', 'scan_options'

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Your"

# Custom CSS Styling (Chartink Atlas Dark Theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    
    /* Top Header Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
        border-bottom: 1px solid #21262d;
        margin-bottom: 15px;
    }
    .top-logo {
        font-size: 22px;
        font-weight: 800;
        color: #38edf8;
    }
    .top-badge {
        background: #1e1b4b;
        color: #818cf8;
        font-size: 11px;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    /* Ci Logo Card */
    .ci-card {
        text-align: center;
        padding: 25px 10px;
        background: #161b22;
        border-radius: 16px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .ci-logo-icon {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
        margin-bottom: 10px;
    }
    
    /* Button Customization */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Login Screen Container */
    .login-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        max-width: 420px;
        margin: 20px auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .badge-pvt {
        background-color: #3d1214;
        color: #ff6b6b;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        border: 1px solid #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)


# =================================----------------------------
# 🔑 1. SIGN IN / LOGIN PAGE (If user is not logged in)
# =================================----------------------------
if not st.session_state.is_logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    
    with col_l2:
        st.markdown("""
        <div style="text-align: center;">
            <div class="ci-logo-icon">Ci</div>
            <h2 style="margin-bottom:0px;">Sign in to your account</h2>
            <p style="color:#8b949e; font-size:14px;">Acharya Atlas Financial Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🌐 Continue With Google", use_container_width=True):
            st.session_state.is_logged_in = True
            st.session_state.user_email = "user@google.com"
            st.success("Successfully logged in with Google!")
            st.rerun()
            
        st.markdown("<div style='text-align:center; color:#8b949e; margin:10px;'>or</div>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email_input = st.text_input("EMAIL", placeholder="name@domain.com")
            pass_input = st.text_input("PASSWORD", type="password", placeholder="••••••••")
            
            c_rem, c_for = st.columns(2)
            with c_rem:
                remember_me = st.checkbox("Remember me", value=True)
            with c_for:
                st.caption("Forgot your password?")
                
            st.write("")
            login_submit = st.form_submit_button("Log in", type="primary", use_container_width=True)
            
            if login_submit:
                if email_input.strip() != "" and pass_input.strip() != "":
                    st.session_state.is_logged_in = True
                    st.session_state.user_email = email_input
                    st.rerun()
                else:
                    st.error("Please enter email and password!")
                    
        if st.button("Register New Account", use_container_width=True):
            st.info("Registration open! Enter email above to log in.")


# =================================----------------------------
# 🚀 2. MAIN APP DASHBOARD (After Login Success)
# =================================----------------------------
else:
    # ---------------------------------------------------------
    # 📌 SIDEBAR MENU (Screens, Charts, Dashboard, Themes)
    # ---------------------------------------------------------
    st.sidebar.title("Chartink ATLAS")
    st.sidebar.caption(f"Logged in as: {st.session_state.user_email}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Search Box in Sidebar
    search_query = st.sidebar.text_input("🔍 Search", placeholder="Ink Chart Search...")
    
    # Expandable Menu Sections
    with st.sidebar.expander("📑 Screens", expanded=True):
        if st.button("➕ Create Scan"):
            st.session_state.view_mode = "scan_options"
            st.rerun()
        st.button("📜 Old Scans")
        
    with st.sidebar.expander("📊 Charts"):
        st.button("📈 Candlestick")
        st.button("📉 P&F Chart")
        
    with st.sidebar.expander("📈 Dashboard", expanded=True):
        if st.button("📂 All Dashboards"):
            st.session_state.view_mode = "home"
            st.rerun()
        st.button("⭐ Watchlists")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("👑 **Premium Features Active**")
    
    # Theme Selection Buttons
    st.sidebar.markdown("🎨 **Theme Options**")
    th_col1, th_col2, th_col3 = st.sidebar.columns(3)
    with th_col1:
        st.button("Light 💡")
    with th_col2:
        st.button("Dark ☾")
    with th_col3:
        st.button("System 🖥️")

    # ---------------------------------------------------------
    # 🏠 HOME VIEW (Acharya Dashboards Studio)
    # ---------------------------------------------------------
    if st.session_state.view_mode == "home":
        # Top Logo Header Bar
        st.markdown("""
        <div class="top-bar">
            <div>
                <span class="top-logo">Acharya</span>
                <span class="top-badge">SCANNER</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hero Analysis Section
        st.markdown("""
        <div class="ci-card">
            <div class="ci-logo-icon">Ci</div>
            <h2 style="margin:5px 0px;">Finance analysis tools</h2>
            <p style="color:#8b949e; font-size:13px;">Customizing stock charts, scans, and widgets — free and fast, so you get the insights you need to improve your trades.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Acharya Studio Header
        st.markdown("### <span style='background:#312e81; color:#c7d2fe; padding:2px 8px; border-radius:4px; font-size:12px;'>ATLAS</span> Acharya Dashboards Studio", unsafe_allow_html=True)
        st.caption("Customize scan result columns, view sector performance, track trends, view multiple scans in a single view.")
        
        st.write("")
        
        # Create Dashboard Primary Button
        if st.button("+ Create Dashboard", type="primary", use_container_width=True):
            st.session_state.view_mode = "create_dashboard"
            st.rerun()
            
        st.write("")
        
        # Tabs: Your | Top | Fav
        t1, t2, t3, t_space = st.columns([1, 1, 1, 3])
        with t1:
            if st.button("Your", type="secondary" if st.session_state.active_tab == "Your" else "tertiary"):
                st.session_state.active_tab = "Your"
                st.rerun()
        with t2:
            if st.button("Top"):
                st.session_state.active_tab = "Top"
                st.rerun()
        with t3:
            if st.button("Fav"):
                st.session_state.active_tab = "Fav"
                st.rerun()
                
        st.markdown("---")
        
        # Dashboard Cards Rendering
        dash_list = st.session_state.dashboards
        if st.session_state.active_tab == "Fav":
            dash_list = [d for d in dash_list if d.get("is_fav", False)]
            
        if len(dash_list) == 0:
            st.info("No dashboards found in this section.")
            
        for idx, d in enumerate(dash_list):
            with st.container():
                c_title, c_opts = st.columns([3, 1])
                
                with c_title:
                    if st.button(f"📌 {d['name']}", key=f"dash_title_{d['id']}"):
                        st.session_state.active_dashboard = d
                        st.session_state.view_mode = "view_dashboard"
                        st.rerun()
                    st.caption(f"Has {len(d.get('widgets', []))} widgets")
                    
                with c_opts:
                    o1, o2, o3 = st.columns(3)
                    with o1:
                        fav_i = "⭐" if d.get("is_fav", False) else "☆"
                        if st.button(fav_i, key=f"fav_{d['id']}"):
                            d["is_fav"] = not d.get("is_fav", False)
                            save_data(st.session_state.dashboards)
                            st.rerun()
                    with o2:
                        if st.button("📋", key=f"cp_{d['id']}"):
                            cp = json.loads(json.dumps(d))
                            cp["id"] = len(st.session_state.dashboards) + 1
                            cp["name"] = f"{d['name']} (COPY)"
                            st.session_state.dashboards.append(cp)
                            save_data(st.session_state.dashboards)
                            st.rerun()
                    with o3:
                        if st.button("🗑️", key=f"del_{d['id']}"):
                            st.session_state.dashboards.pop(idx)
                            save_data(st.session_state.dashboards)
                            st.rerun()
                            
                st.markdown("---")

    # ---------------------------------------------------------
    # 🛠️ 3. CREATE DASHBOARD VIEW
    # ---------------------------------------------------------
    elif st.session_state.view_mode == "create_dashboard":
        if st.button("⬅️ Back"):
            st.session_state.view_mode = "home"
            st.rerun()
            
        st.title("🛠️ Create New Dashboard")
        st.markdown("---")
        
        with st.form("create_dash"):
            dash_title = st.text_input("Name", placeholder="Title (e.g. Tomato or IBB Scanner)")
            is_private_check = st.checkbox("Private Premium", value=True)
            
            st.write("")
            cb1, cb2 = st.columns(2)
            with cb2:
                btn_save = st.form_submit_button("Create", type="primary", use_container_width=True)
                
            if btn_save:
                if dash_title.strip() != "":
                    new_item = {
                        "id": len(st.session_state.dashboards) + 1,
                        "name": dash_title.upper(),
                        "desc": "Has 0 widgets",
                        "is_private": is_private_check,
                        "is_fav": False,
                        "widgets": []
                    }
                    st.session_state.dashboards.append(new_item)
                    save_data(st.session_state.dashboards)
                    st.session_state.view_mode = "home"
                    st.rerun()
                else:
                    st.error("Please enter a Dashboard Name!")

    # ---------------------------------------------------------
    # 📊 4. VIEW SINGLE DASHBOARD
    # ---------------------------------------------------------
    elif st.session_state.view_mode == "view_dashboard":
        active = st.session_state.active_dashboard
        
        if st.button("⬅️ Back to Dashboards"):
            st.session_state.view_mode = "home"
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
                st.info(f"Loaded Template: {w['type']} | Fetching Live Market Breakouts...")
                st.markdown("---")
                
            if st.button("➕ Add Another Widget"):
                st.session_state.view_mode = "scan_options"
                st.rerun()

    # ---------------------------------------------------------
    # 📑 5. SCAN OPTIONS / TEMPLATES VIEW
    # ---------------------------------------------------------
    elif st.session_state.view_mode == "scan_options":
        active = st.session_state.active_dashboard
        
        if st.button("❌ Close"):
            st.session_state.view_mode = "view_dashboard" if active else "home"
            st.rerun()
                
        st.markdown("<h2 style='text-align: center;'>Create a new scan/chart</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button("⟇ ➕ New Scan (Start Afresh)", use_container_width=True):
            if active:
                active['widgets'].append({"name": "Custom New Scan", "type": "Custom Scratch"})
                save_data(st.session_state.dashboards)
                st.session_state.view_mode = "view_dashboard"
            else:
                st.session_state.view_mode = "home"
            st.rerun()

        st.write("<br>", unsafe_allow_html=True)
        st.subheader("Start from a template")

        templates = [
            ("📈 Sector Advances %", "Sector Advances"),
            ("📊 Stocks near 52 week high", "52W High"),
            ("⚡ Top gainers %", "Top Gainers"),
            ("🌐 Industry Stocks at 52-wk high", "Industry 52W High"),
            ("📉 Average marketcap RSI", "Marketcap RSI"),
            ("📌 Stocks above VWAP", "Above VWAP"),
            ("📈 Todays Volume vs 50 SMA volume", "Volume vs 50 SMA")
        ]

        for temp_label, temp_code in templates:
            if st.button(temp_label, key=f"btn_{temp_code}", use_container_width=True):
                if active:
                    active['widgets'].append({"name": temp_label, "type": temp_code})
                    save_data(st.session_state.dashboards)
                    st.session_state.view_mode = "view_dashboard"
                else:
                    st.session_state.view_mode = "home"
                st.rerun()
    
