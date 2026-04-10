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

    # Test user credentials
    TEST_PHONE = "8888888888"
    TEST_PASSWORD = "Test@123"
    TEST_NAME = "Test User"
    TEST_EMAIL = "test@doorstep.com"

    print(f"Connecting to database...", flush=True)
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables verified.", flush=True)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Create Admin
        result = await session.execute(select(User).where(User.phone == ADMIN_PHONE))
        if not result.scalars().first():
            admin = User(
                id=uuid.uuid4(),
                phone=ADMIN_PHONE,
                email=ADMIN_EMAIL,
                full_name=ADMIN_NAME,
                role="admin",
                password_hash=get_password_hash(ADMIN_PASSWORD),
                is_phone_verified=True,
                status="active"
            )
            session.add(admin)
            print(f"✅ Admin created: phone={ADMIN_PHONE}, password={ADMIN_PASSWORD}", flush=True)
        else:
            print(f"Admin {ADMIN_PHONE} already exists, skipping.", flush=True)

        # Create Test Customer
        result = await session.execute(select(User).where(User.phone == TEST_PHONE))
        if not result.scalars().first():
            test_user = User(
                id=uuid.uuid4(),
                phone=TEST_PHONE,
                email=TEST_EMAIL,
                full_name=TEST_NAME,
                role="customer",
                password_hash=get_password_hash(TEST_PASSWORD),
                is_phone_verified=True,
                status="active"
            )
            session.add(test_user)
            print(f"✅ Test user created: phone={TEST_PHONE}, password={TEST_PASSWORD}", flush=True)
        else:
            print(f"Test user {TEST_PHONE} already exists, skipping.", flush=True)

        await session.commit()

    await engine.dispose()
    print("\n🎉 Seeding complete!", flush=True)

if __name__ == "__main__":
    asyncio.run(seed_admin())
