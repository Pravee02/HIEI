import requests
import streamlit as st

import os



# FORCE USE RENDER URL
API_URL = "https://hiei.onrender.com"



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
