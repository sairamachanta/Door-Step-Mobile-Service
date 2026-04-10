import requests
import json

base_url = "http://localhost:8000/api"

def test_auth_flow():
    # 1. Signup
    signup_url = f"{base_url}/auth/signup"
    signup_data = {
        "full_name": "Unique Test User",
        "phone": "9000000000",
        "password": "Password123!",
        "email": "unique_test@example.com"
    }
    print(f"Signing up: {signup_data['phone']}...")
    try:
        response = requests.post(signup_url, json=signup_data)
        print(f"Signup Result: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Signup Exception: {e}")

    # 2. Login
    login_url = f"{base_url}/auth/login"
    login_data = {
        "phone": "9000000000",
        "password": "Password123!"
    }
    print(f"\nLogging in: {login_data['phone']}...")
    try:
        response = requests.post(login_url, json=login_data)
        print(f"Login Result: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Login Exception: {e}")

if __name__ == "__main__":
    test_auth_flow()
