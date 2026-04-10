
import asyncio
from app.database import engine
from sqlalchemy import text
import os

async def check():
    log_path = "/home/sairam_achanta/Documents/Doorstep_mobile_services/backend/db_audit.log"
    try:
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT phone, role, status, is_phone_verified FROM users WHERE phone IN ('9000000001', '9000000002', '9000000003')"))
            rows = res.fetchall()
            with open(log_path, "w") as f:
                f.write(f"Found {len(rows)} users\n")
                for row in rows:
                    f.write(f"Phone: {row.phone} | Role: {row.role} | Status: {row.status} | Verified: {row.is_phone_verified}\n")
            
            # Also check if there are ANY users
            res_all = await conn.execute(text("SELECT count(*) FROM users"))
            count = res_all.scalar()
            with open(log_path, "a") as f:
                f.write(f"Total users in DB: {count}\n")

    except Exception as e:
        with open(log_path, "w") as f:
            f.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(check())
