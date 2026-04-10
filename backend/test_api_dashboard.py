import asyncio
import httpx
from datetime import datetime
import asyncpg

async def test():
    phone = "99" + str(int(datetime.now().timestamp()))[:8]
    async with httpx.AsyncClient() as client:
        # Signup
        res = await client.post("http://localhost:8000/api/auth/signup", json={
            "phone": phone,
            "full_name": "Test User",
            "password": "password123",
            "email": f"test{phone}@example.com"
        })
        
        # Get OTP from DB
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5432/doorstep_services")
        otp = await conn.fetchval('SELECT otp_code FROM otp_verifications WHERE phone = $1 ORDER BY created_at DESC LIMIT 1', phone)
        await conn.close()
        
        # Verify OTP
        res2 = await client.post("http://localhost:8000/api/auth/verify-otp", json={
            "phone": phone,
            "otp_code": otp,
            "otp_type": "signup"
        })
        token = res2.json()["access_token"]
        
        # Call Dashboard Stats
        res3 = await client.get("http://localhost:8000/api/dashboard/stats", headers={"Authorization": f"Bearer {token}"})
        print("Dashboard Stats Status:", res3.status_code)
        if res3.status_code != 200:
            print("Dashboard Stats Error:", res3.text)

if __name__ == "__main__":
    asyncio.run(test())
