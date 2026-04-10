import asyncio
import httpx
from datetime import datetime
import asyncpg

async def test():
    phone = "99" + str(int(datetime.now().timestamp() * 100))[-8:]
    async with httpx.AsyncClient() as client:
        # Signup
        r1 = await client.post("http://localhost:8000/api/auth/signup", json={
            "phone": phone,
            "full_name": "Test User",
            "password": "password123",
            "email": f"test{phone}@example.com"
        })
        if r1.status_code != 200:
            print("Signup Error:", r1.text)
            return
            
        # Get OTP
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5432/doorstep_services")
        otp = await conn.fetchval('SELECT otp_code FROM otp_verifications WHERE phone = $1 ORDER BY created_at DESC LIMIT 1', phone)
        await conn.close()
        
        # Verify
        res2 = await client.post("http://localhost:8000/api/auth/verify-otp", json={
            "phone": phone,
            "otp_code": otp,
            "otp_type": "signup"
        })
        if res2.status_code != 200:
            print("Verify Error:", res2.text)
            return
            
        token = res2.json()["access_token"]
        
        # API Calls
        endpoints = [
            "/dashboard/stats",
            "/bookings/active",
            "/bookings/recent?limit=3",
            "/dashboard/quick-actions",
            "/banners/active"
        ]
        
        for ep in endpoints:
            r = await client.get(f"http://localhost:8000/api{ep}", headers={"Authorization": f"Bearer {token}"})
            print(f"[{ep}]: {r.status_code}")
            if r.status_code != 200:
                print(f"   -> {r.text}")

if __name__ == "__main__":
    asyncio.run(test())
