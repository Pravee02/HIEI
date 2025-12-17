import requests

BASE_URL = "http://127.0.0.1:5000/api/auth"

def test_auth():
    import time
    unique_id = int(time.time())
    username = f"testuser_{unique_id}"
    print(f"Testing Auth for: {username}")
    
    # 1. Register User
    print("Testing Registration...")
    reg_payload = {
        "username": username,
        "password": "password123",
        "phone": "1234567890",
        "address": "123 Test St",
        "household_group": "Urban Middle"
    }
    try:
        r = requests.post(f"{BASE_URL}/register/user", json=reg_payload)
        print(f"Registration Status: {r.status_code}")
        print(f"Registration Response: {r.json()}")
    except Exception as e:
        print(f"Registration Failed: {e}")
        if 'r' in locals(): print(r.text)

    # 2. Login User
    print("\nTesting Login...")
    login_payload = {
        "username": username,
        "password": "password123"
    }
    try:
        r = requests.post(f"{BASE_URL}/login/user", json=login_payload)
        print(f"Login Status: {r.status_code}")
        print(f"Login Response: {r.json()}")
    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_auth()
