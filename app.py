import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Scanner Dashboard")

# Session State Initialization
if "dashboards" not in st.session_state:
    st.session_state.dashboards = []

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "create"  # Options: 'create', 'saved_list', 'view_dashboard'

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
    .card-box {
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        background-color: #161b22;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. CREATE DASHBOARD PAGE (Form)
# -------------------------------------------------------------
if st.session_state.view_mode == "create":
    st.title("🛠️ Create New Dashboard")
    st.write("Fill details below to create your personal scanner dashboard.")
    st.markdown("---")
    
    with st.form("create_dash_form"):
        dash_name = st.text_input("📌 Scanner / Dashboard Name", placeholder="Enter scanner name (e.g. Tomato)")
        dash_desc = st.text_area("📝 Description (Optional)", placeholder="Write a brief description...")
        is_pvt = st.checkbox("🔒 Make Dashboard Private", value=True)
        
        st.write("")
        submit_btn = st.form_submit_button("🚀 Save / Create Dashboard", use_container_width=True)

        if submit_btn:
            if dash_name.strip() != "":
                new_dash = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": dash_name,
                    "desc": dash_desc,
                    "is_private": is_pvt,
                    "is_fav": False
                }
                st.session_state.dashboards.append(new_dash)
                st.session_state.active_dashboard = new_dash
                st.session_state.view_mode = "saved_list"
                st.rerun()
            else:
                st.error("Please enter a Scanner Name!")

# -------------------------------------------------------------
# 2. DASHBOARD SAVED / CREATED PAGE (Image 2 View)
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
                # Dashboard Name
                if st.button(f"📌 {d['name']}", key=f"open_dash_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.session_state.view_mode = "view_dashboard"
                    st.rerun()
                
                # Private / Public Label
                if d['is_private']:
                    st.markdown('<span class="badge-private">🔒 Private</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-public">🌐 Public</span>', unsafe_allow_html=True)
                
                if d['desc']:
                    st.caption(d['desc'])
            
            with col2:
                # Favorite, Copy, Delete Buttons
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
# 3. DETAILED DASHBOARD SCANNER VIEW
# -------------------------------------------------------------
elif st.session_state.view_mode == "view_dashboard":
    active = st.session_state.active_dashboard
    
    if st.button("⬅️ Back to Saved List"):
        st.session_state.view_mode = "saved_list"
        st.rerun()
        
    st.title(f"📊 {active['name']}")
    if active['is_private']:
        st.markdown('<span class="badge-private">🔒 Private</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-public">🌐 Public</span>', unsafe_allow_html=True)
        
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 BULLISH BREAKOUTS")
        st.info("Scanner data loading...")
    with col2:
        st.subheader("🔴 BEARISH BREAKOUTS")
        st.info("Scanner data loading...")
    
