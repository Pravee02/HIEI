import requests
import streamlit as st

import os


# Try to get from st.secrets first (Streamlit Cloud), then os.getenv, then localhost default
try:
    API_URL = st.secrets["API_URL"]
    print(f"DEBUG: Using st.secrets: {API_URL}")
except:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
    print(f"DEBUG: Using os.getenv/default: {API_URL}")

# DEBUG: Temporarily show this on screen for user to verify
# st.warning(f"DEBUG: Backend connected to: {API_URL}")


def check_backend_status():
    try:
        r = requests.get(f"{API_URL}/")
        return r.status_code == 200
    except:
        return False

def login_user(username, password):
    try:
        r = requests.post(f"{API_URL}/api/auth/login", json={"username": username, "password": password})
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def register_user(username, password, role):
    try:
        r = requests.post(f"{API_URL}/api/auth/register", json={"username": username, "password": password, "role": role})
        return r.status_code == 201, r.json()
    except Exception as e:
        return False, {"message": str(e)}
