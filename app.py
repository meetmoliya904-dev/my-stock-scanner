import streamlit as st

# Page Configuration
st.set_page_config(layout="wide", page_title="Stoxify - Create Dashboard")

# Session State Initialization
if "dashboards" not in st.session_state:
    st.session_state.dashboards = []

if "active_dashboard" not in st.session_state:
    st.session_state.active_dashboard = None

# Custom CSS
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
    }
    .badge-public {
        background-color: #123d24;
        color: #51cf66;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 13px;
        border: 1px solid #51cf66;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🟢 ACTIVE DASHBOARD VIEW (Created Dashboard Page)
# -------------------------------------------------------------
if st.session_state.active_dashboard:
    active = st.session_state.active_dashboard
    
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Back"):
            st.session_state.active_dashboard = None
            st.rerun()
            
    st.title(f"📊 Dashboard: {active['name']}")
    
    if active['is_private']:
        st.markdown('<span class="badge-private">🔒 Private Dashboard</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-public">🌐 Public Dashboard</span>', unsafe_allow_html=True)
        
    st.write("---")
    
    # Scanner Data Display Space
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 BULLISH BREAKOUTS")
        st.info("Scanner Ready! Live stock data loading...")
    with col2:
        st.subheader("🔴 BEARISH BREAKOUTS")
        st.info("Scanner Ready! Live stock data loading...")

# -------------------------------------------------------------
# ➕ MAIN CREATE DASHBOARD PAGE
# -------------------------------------------------------------
else:
    st.title("🛠️ Create New Dashboard")
    st.write("Fill details below to create your custom stock scanner dashboard.")
    st.markdown("---")
    
    with st.form("create_dash_form"):
        dash_name = st.text_input("📌 Scanner / Dashboard Name", placeholder="Enter name (e.g. Tomato, Breakout 15m)")
        dash_desc = st.text_area("📝 Description (Optional)", placeholder="Write a brief description...")
        is_pvt = st.checkbox("🔒 Make Dashboard Private", value=True)
        
        st.write("")
        submit_btn = st.form_submit_button("🚀 Create Dashboard", use_container_width=True)

        if submit_btn:
            if dash_name.strip() != "":
                new_dash = {
                    "id": len(st.session_state.dashboards) + 1,
                    "name": dash_name,
                    "desc": dash_desc,
                    "is_private": is_pvt
                }
                st.session_state.dashboards.append(new_dash)
                st.session_state.active_dashboard = new_dash
                st.success(f"Dashboard '{dash_name}' Created Successfully!")
                st.rerun()
            else:
                st.error("Please enter a Dashboard Name!")

    # Show Created Dashboards List below if available
    if len(st.session_state.dashboards) > 0:
        st.markdown("---")
        st.subheader("📋 Your Created Dashboards")
        for d in st.session_state.dashboards:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**📌 {d['name']}** - _({ 'Private' if d['is_private'] else 'Public' })_")
            with col2:
                if st.button("Open ↗️", key=f"open_{d['id']}"):
                    st.session_state.active_dashboard = d
                    st.rerun()
                    
