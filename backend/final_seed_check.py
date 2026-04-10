
import asyncio
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from app.database import engine, SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash
from sqlalchemy import select
import uuid

async def final_check():
    log_path = "/home/sairam_achanta/Documents/Doorstep_mobile_services/backend/final_seed_report.txt"
    with open(log_path, "w") as f:
        f.write("Starting final check...\n")

    try:
        # 1. Ensure columns exist
        async with engine.begin() as conn:
            res = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"))
            columns = [row[0] for row in res.fetchall()]
            if 'status' not in columns:
                await conn.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR DEFAULT 'active'"))
            if 'role' not in columns:
                await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'customer'"))
            await conn.commit()

        # 2. Seed Users
        DEFAULT_USERS = [
            {"phone": "9000000001", "name": "Super Admin", "role": "superadmin"},
            {"phone": "9000000002", "name": "Admin", "role": "admin"},
            {"phone": "9000000003", "name": "Customer", "role": "customer"},
        ]
        password_hash = get_password_hash("password123")

        async with SessionLocal() as session:
            for u_data in DEFAULT_USERS:
                result = await session.execute(select(User).where(User.phone == u_data["phone"]))
                user = result.scalars().first()
                if not user:
                    new_user = User(
                        id=uuid.uuid4(),
                        phone=u_data["phone"],
                        full_name=u_data["name"],
                        role=u_data["role"],
                        password_hash=password_hash,
                        is_phone_verified=True,
                        status="active"
                    )
                    session.add(new_user)
                    with open(log_path, "a") as f:
                        f.write(f"Created user: {u_data['phone']}\n")
                else:
                    user.status = "active" # Ensure it's active
                    user.password_hash = password_hash # Reset password just in case
                    with open(log_path, "a") as f:
                        f.write(f"User {u_data['phone']} already exists. Status set to active.\n")
            await session.commit()
        
        with open(log_path, "a") as f:
            f.write("Final check COMPLETE.\n")

    except Exception as e:
        with open(log_path, "a") as f:
            f.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    from sqlalchemy import text # Import here inside
    asyncio.run(final_check())
