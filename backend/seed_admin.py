"""
Seed an admin user directly on the production Render database.
Run this via Render Shell or locally with the production DATABASE_URL.

Usage (from Render Shell):
  python seed_admin.py

Usage (locally, with production DATABASE_URL):
  DATABASE_URL="postgresql+asyncpg://..." python seed_admin.py
"""
import asyncio
import uuid
import sys
import os

async def seed_admin():
    # Import after setting up
    from app.config import settings
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import select
    from app.models.user import User
    from app.utils.security import get_password_hash
    from app.database import Base

    # Admin credentials
    ADMIN_PHONE = "9999999999"
    ADMIN_PASSWORD = "Admin@123"
    ADMIN_NAME = "Super Admin"
    ADMIN_EMAIL = "admin@doorstep.com"

    # Technician credentials
    TECH_PHONE = "7777777777"
    TECH_PASSWORD = "Tech@123"
    TECH_NAME = "Tech User"
    TECH_EMAIL = "tech@doorstep.com"

    # Customer credentials
    CUST_PHONE = "8888888888"
    CUST_PASSWORD = "User@123"
    CUST_NAME = "Test Customer"
    CUST_EMAIL = "customer@doorstep.com"

    print(f"Connecting to database...", flush=True)
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables verified.", flush=True)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    users_to_seed = [
        {"phone": ADMIN_PHONE, "password": ADMIN_PASSWORD, "name": ADMIN_NAME, "email": ADMIN_EMAIL, "role": "admin"},
        {"phone": TECH_PHONE, "password": TECH_PASSWORD, "name": TECH_NAME, "email": TECH_EMAIL, "role": "technician"},
        {"phone": CUST_PHONE, "password": CUST_PASSWORD, "name": CUST_NAME, "email": CUST_EMAIL, "role": "customer"},
    ]

    async with async_session() as session:
        for u in users_to_seed:
            result = await session.execute(select(User).where(User.phone == u["phone"]))
            if not result.scalars().first():
                user = User(
                    id=uuid.uuid4(),
                    phone=u["phone"],
                    email=u["email"],
                    full_name=u["name"],
                    role=u["role"],
                    password_hash=get_password_hash(u["password"]),
                    is_phone_verified=True,
                    status="active"
                )
                session.add(user)
                print(f"✅ {u['role'].upper()} created: phone={u['phone']}, password={u['password']}", flush=True)
            else:
                print(f"⏩ {u['role'].upper()} {u['phone']} already exists, skipping.", flush=True)

        await session.commit()

    await engine.dispose()
    print("\n🎉 Seeding complete!", flush=True)

if __name__ == "__main__":
    asyncio.run(seed_admin())
