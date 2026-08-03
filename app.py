import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Dashboard Creator")

# Session State Initializations
if "dashboards" not in st.session_state:
    st.session_state.dashboards = [
        {
            "id": 1,
            "name": "Tomato",
            "desc": "Daily breakout scanner for cash segment",
            "is_private": True,
            "is_fav": True
        }
    ]

if "show_create_modal" not in st.session_state:
    st.session_state.show_create_modal = False

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

# Custom CSS for Chartink Style UI
st.markdown("""
<style>
    /* Card Styles */
    .dashboard-card {
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        background-color: #161b22;
        margin-bottom: 15px;
    }
    .badge-private {
        background-color: #3d1214;
        color: #ff6b6b;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        border: 1px solid #ff6b6b;
    }
    .badge-public {
        background-color: #123d24;
        color: #51cf66;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        border: 1px solid #51cf66;
    }
    /* Floating Plus Button */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #0080FF;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 30px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        cursor: pointer;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("📊 Stoxify - Atlas Dashboards")

# -------------------------------------------------------------
# 1. CREATE NEW DASHBOARD FORM (Modal View)
# -------------------------------------------------------------
if st.session_state.show_create_modal:
    st.markdown("### ➕ Create New Dashboard")
    with st.form("create_dash_form"):
        dash_name = st.text_input("Dashboard Name", placeholder="Ex. Tomato, Breakout 15m")
        dash_desc = st.text_area("Description (Optional)", placeholder="Write a short description...")
        is_pvt = st.checkbox("🔒 Make Dashboard Private", value=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            submit_btn = st.form_submit_button("Submit / Save")
        with col_btn2:
            cancel_btn = st.form_submit_button("Cancel")

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
                st.session_state.show_create_modal = False
                st.success(f"Dashboard '{dash_name}' Created Successfully!")
                st.rerun()
            else:
                st.error("Dashboard Name is required!")
        if cancel_btn:
            st.session_state.show_create_modal = False
            st.rerun()

    st.markdown("---")

# -------------------------------------------------------------
# 2. ACTIVE DASHBOARD VIEW (If Selected)
# -------------------------------------------------------------
if st.session_state.active_dashboard:
    active = st.session_state.active_dashboard
    st.button("⬅️ Back to All Dashboards", on_click=lambda: st.session_state.update(active_dashboard=None))
    
    st.header(f"📈 Dashboard: {active['name']}")
    if active['is_private']:
        st.markdown('<span class="badge-private">🔒 PRIVATE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-public">🌐 PUBLIC</span>', unsafe_allow_html=True)
    
    st.caption(active['desc'])
    st.write("---")
    
    # Grid Layout for Widgets inside Dashboard
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 BULLISH BREAKOUTS")
        st.info("No stocks found in scanner.")
    with col2:
        st.subheader("🔴 BEARISH BREAKOUTS")
        st.info("No stocks found in scanner.")

# -------------------------------------------------------------
# 3. ALL DASHBOARDS LIST (Image 2 View)
# -------------------------------------------------------------
else:
    st.subheader("📋 My Dashboards")
    
    if len(st.session_state.dashboards) == 0:
        st.info("No dashboards created yet. Click the (+) button to create one!")
    
    for idx, d in enumerate(st.session_state.dashboards):
        with st.container():
            col_main, col_actions = st.columns([3, 1])
            
            with col_main:
                # Clickable Name
                if st.button(f"📌 {d['name']}", key=f"title_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.rerun()
                
                # Private / Public Label
                if d['is_private']:
                    st.markdown('<span class="badge-private">🔒 Private</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-public">🌐 Public</span>', unsafe_allow_html=True)
                
                st.write(f"_{d['desc']}_" if d['desc'] else "_No description_")
            
            with col_actions:
                # Action Buttons (Favorite, Copy, Delete)
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    fav_icon = "⭐" if d['is_fav'] else "☆"
                    if st.button(fav_icon, key=f"fav_{d['id']}"):
                        d['is_fav'] = not d['is_fav']
                        st.rerun()
                
                with c2:
                    if st.button("📋", key=f"copy_{d['id']}"):
                        copied_dash = d.copy()
                        copied_dash['id'] = len(st.session_state.dashboards) + 1
                        copied_dash['name'] = f"{d['name']} (Copy)"
                        st.session_state.dashboards.append(copied_dash)
                        st.success(f"Copied '{d['name']}'!")
                        st.rerun()
                        
                with c3:
                    if st.button("🗑️", key=f"del_{d['id']}"):
                        st.session_state.dashboards.pop(idx)
                        st.rerun()
            
            st.markdown("---")

# -------------------------------------------------------------
# 4. PLUS (+) FLOATING BUTTON (Image 3 View)
# -------------------------------------------------------------
st.write("<br><br>", unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns([8, 1, 1])
with col_p3:
    if st.button("➕ Create New", type="primary", use_container_width=True):
        st.session_state.show_create_modal = True
        st.rerun()
        
