import streamlit as st
import requests

from utils.api import API_URL

# Re-append /api/auth since the original variable included it
AUTH_API_URL = f"{API_URL}/api/auth"

def user_login():
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login as User"):
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
    st.header("User Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    household_group = st.selectbox("Household Group", ["Urban Poor", "Urban Rich", "Rural Poor", "Rural Rich"])
    
    if st.button("Register User"):
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
    st.header("Policy Maker Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login as Policy Maker"):
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
    st.header("Policy Maker Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")
    policy_area = st.text_input("Policy Area (e.g., Food Security, Finance)")
    
    if st.button("Register Policy Maker"):
        try:
            payload = {"username": username, "password": password, "phone": phone, "policy_area": policy_area}
            res = requests.post(f"{AUTH_API_URL}/register/policy", json=payload)
            if res.status_code == 201:
                st.success("Registration Successful! Please Login.")
            else:
                st.error(res.json().get("error", "Registration failed"))
        except Exception as e:
            st.error(f"Connection Error: {e}")
