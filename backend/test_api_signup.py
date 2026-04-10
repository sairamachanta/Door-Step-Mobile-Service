import asyncio
import httpx
from datetime import datetime
import asyncpg

async def test():
    phone = "99" + str(int(datetime.now().timestamp()))[:8]
    print(f"Signing up with phone: {phone}")
    async with httpx.AsyncClient() as client:
        # Signup
        res = await client.post("http://localhost:8000/api/auth/signup", json={
            "phone": phone,
            "full_name": "Test User",
            "password": "password123",
            "email": f"test{phone}@example.com"
        })
        print("Signup Response Status:", res.status_code)
        
        # Get OTP from DB
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5432/doorstep_services")
        otp = await conn.fetchval('SELECT otp_code FROM otp_verifications WHERE phone = $1 ORDER BY created_at DESC LIMIT 1', phone)
        await conn.close()
        print("OTP:", otp)
        
        # Verify OTP
        res2 = await client.post("http://localhost:8000/api/auth/verify-otp", json={
            "phone": phone,
            "otp_code": otp,
            "otp_type": "signup"
        })
        print("Verify Response Status:", res2.status_code)
        print("Verify Response JSON:", res2.json())

if __name__ == "__main__":
    asyncio.run(test())
