import streamlit as st
import requests
import os
from utils.api import API_URL

# Re-append /api/auth since the original variable included it
AUTH_API_URL = f"{API_URL}/api/auth"

def load_local_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

def user_login():
    load_local_css()
    
    # Centered Layout
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c2:
        st.markdown("""
            <div class="auth-header">
                <span class="secure-icon">🔐</span>
                <h2>Citizen Login</h2>
                <p>Secure access to your household finance dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Login to Dashboard", type="primary", use_container_width=True):
            try:
                res = requests.post(f"{AUTH_API_URL}/login/user", json={"username": username, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.user_token = data['token']
                    st.session_state.user_id = data['user_id']
                    st.session_state.username = data['username']
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    try:
                        err_msg = res.json().get("error", "Login failed")
                    except:
                        err_msg = f"Error {res.status_code}: {res.text[:100]}"
                    st.error(err_msg)
            except Exception as e:
                st.error(f"Connection Error: {e}")

def user_register():
    load_local_css()
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
            <div class="auth-header">
                <span class="secure-icon">📝</span>
                <h2>Citizen Registration</h2>
                <p>Join the platform to track inflation impact</p>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        household_group = st.selectbox("Household Group", ["Urban Poor", "Urban Rich", "Rural Poor", "Rural Rich"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Create Account", type="primary", use_container_width=True):
            try:
                payload = {
                    "username": username, 
                    "password": password, 
                    "phone": phone, 
                    "address": address,
                    "household_group": household_group
                }
                res = requests.post(f"{AUTH_API_URL}/register/user", json=payload)
                if res.status_code == 201:
                    st.success("Registration Successful! Please navigate to 'User Login' to continue.")
                else:
                    try:
                        err_msg = res.json().get("error", "Registration failed")
                    except:
                        err_msg = f"Error {res.status_code}: {res.text[:100]}"
                    st.error(err_msg)
            except Exception as e:
                st.error(f"Connection Error: {e}")

def policy_login():
    load_local_css()
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
            <div class="auth-header">
                <span class="secure-icon">🏛️</span>
                <h2>Policy Maker Login</h2>
                <p>Authorized access for government administrators</p>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Login as Policy Maker", type="primary", use_container_width=True):
            try:
                res = requests.post(f"{AUTH_API_URL}/login/policy", json={"username": username, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.pm_token = data['token']
                    st.session_state.pm_id = data['pm_id']
                    st.session_state.username = data['username']
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error(res.json().get("error", "Login failed"))
            except Exception as e:
                st.error(f"Connection Error: {e}")

def policy_register():
    load_local_css()
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
            <div class="auth-header">
                <span class="secure-icon">📋</span>
                <h2>Policy Maker Registration</h2>
                <p>Register as a new administrator</p>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone Number")
        policy_area = st.text_input("Policy Area (e.g., Food Security, Finance)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Register Account", type="primary", use_container_width=True):
            try:
                payload = {"username": username, "password": password, "phone": phone, "policy_area": policy_area}
                res = requests.post(f"{AUTH_API_URL}/register/policy", json=payload)
                if res.status_code == 201:
                    st.success("Registration Successful! Please Login.")
                else:
                    st.error(res.json().get("error", "Registration failed"))
            except Exception as e:
                st.error(f"Connection Error: {e}")
