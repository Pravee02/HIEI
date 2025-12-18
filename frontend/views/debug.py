import streamlit as st
import requests

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

# --- Debug / Admin Panel ---
# --- Debug / Admin Panel ---
def display_debug_panel():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛠️ Admin & Debug")
    
    # Use an expander instead of checkbox to keep it clean but accessible
    with st.sidebar.expander("Debug Info", expanded=False):
        st.write("Session State:")
        st.json(st.session_state)
        
        st.write("API Base:", API_BASE)
        
        if st.button("Check Backend Health"):
            try:
                r = requests.get(f"{API_URL}/")
                st.success(f"Backend Status: {r.status_code}")
            except Exception as e:
                st.error(f"Backend Error: {e}")
