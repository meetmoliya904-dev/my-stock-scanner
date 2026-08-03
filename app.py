import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Atlas Dashboard")

# Session State Initialization
if "dashboards" not in st.session_state:
    st.session_state.dashboards = [
        {"id": 1, "name": "Tomato", "desc": "Daily Breakout Scanner", "is_private": True, "is_fav": False, "widgets": []}
    ]

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "saved_list"  # Modes: 'create', 'saved_list', 'dashboard_view', 'add_widget'

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

# Custom CSS Styling
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
    /* Plus Button Styling */
    div.stButton > button[kind="primary"] {
        background-color: #8A2BE2 !important;
        color: white !important;
        font-size: 28px !important;
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        margin: 0 auto;
        display: block;
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
        dash_name = st.text_input("📌 Scanner Name", placeholder="Enter scanner name (e.g. Tomato)")
        dash_desc = st.text_area("📝 Description (Optional)", placeholder="Write description...")
        is_pvt = st.checkbox("🔒 Make Private", value=True)
        
        st.write("")
        submit_btn = st.form_submit_button("🚀 Save / Create Dashboard", use_container_width=True)

        if submit_btn:
            if dash_name.strip() != "":
                new_dash = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": dash_name,
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
                # Name Tab Click -> Opens Page 3 (Dashboard View)
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
# 3. DASHBOARD PAGE (With Center PLUS '+' Button)
# -------------------------------------------------------------
elif st.session_state.view_mode == "dashboard_view":
    active = st.session_state.active_dashboard
    
    col_b, col_h = st.columns([1, 5])
    with col_b:
        if st.button("⬅️ Back"):
            st.session_state.view_mode = "saved_list"
            st.rerun()
            
    st.title(f"📊 Dashboard: {active['name']}")
    st.markdown("---")
    
    # If no widgets created yet, show Center PLUS (+) Button
    if len(active['widgets']) == 0:
        st.write("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>No Widgets Added Yet</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Click '+' below to add your first scanner table/widget.</p>", unsafe_allow_html=True)
        st.write("")
        
        # Big Plus Button in Center
        col_p1, col_p2, col_p3 = st.columns([2, 1, 2])
        with col_p2:
            if st.button("➕", type="primary", use_container_width=True):
                st.session_state.view_mode = "add_widget"
                st.rerun()
    else:
        # Display existing widgets
        for w in active['widgets']:
            st.subheader(f"📈 {w['name']}")
            st.info("Live Scanner Table Data Loading...")
        
        st.write("---")
        if st.button("➕ Add Another Widget"):
            st.session_state.view_mode = "add_widget"
            st.rerun()

# -------------------------------------------------------------
# 4. NEW WIDGET / TABLE CREATION PAGE (Opens on Plus Click)
# -------------------------------------------------------------
elif st.session_state.view_mode == "add_widget":
    active = st.session_state.active_dashboard
    
    st.title(f"⚡ Add New Table / Widget to '{active['name']}'")
    st.write("Configure your stock scanner table rules below.")
    st.markdown("---")
    
    with st.form("add_widget_form"):
        w_name = st.text_input("📌 Widget / Table Title", placeholder="e.g. Bullish Breakout 15m")
        w_type = st.selectbox("📊 Select Segment / Filter Type", ["Bullish Stocks", "Bearish Stocks", "Bullish Sectors", "Bearish Sectors"])
        
        st.write("")
        create_w_btn = st.form_submit_button("✅ Add Table to Dashboard", use_container_width=True)
        
        if create_w_btn:
            if w_name.strip() != "":
                active['widgets'].append({"name": w_name, "type": w_type})
                st.session_state.view_mode = "dashboard_view"
                st.rerun()
            else:
                st.error("Please enter a Widget Title!")
                
    st.write("")
    if st.button("❌ Cancel"):
        st.session_state.view_mode = "dashboard_view"
        st.rerun()
        
