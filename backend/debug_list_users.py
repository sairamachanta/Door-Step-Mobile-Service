import requests
from app.config import settings

BASE_API_URL = settings.BASE_API_URL
admin_phone = settings.ROOT_ADMIN_PHONE
password = settings.ROOT_ADMIN_PASSWORD

def test():
    resp = requests.post(f"{BASE_API_URL}/auth/login", json={"phone": admin_phone, "password": password})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(f"{BASE_API_URL}/admin/users?role=customer", headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test()
