import asyncio
import uuid
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import User
from app.utils.security import get_password_hash
from app.config import settings

async def create_admin():
    print("=== Create Superadmin ===")
    phone = input("Enter admin phone number: ").strip()
    password = input("Enter admin password: ").strip()
    full_name = input("Enter admin full name: ").strip()

    if not phone or not password or not full_name:
        print("All fields are required.")
        return

    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.phone == phone))
        existing_user = result.scalars().first()
        
        if existing_user:
            print(f"User {phone} already exists. Updating their role to admin and resetting their password...")
            existing_user.role = "admin"
            existing_user.password_hash = get_password_hash(password)
        else:
            print(f"Creating new admin user: {phone}...")
            new_user = User(
                id=uuid.uuid4(),
                phone=phone,
                full_name=full_name,
                role="admin",
                password_hash=get_password_hash(password),
                is_phone_verified=True,
                status="active"
            )
            session.add(new_user)
        
        await session.commit()
    
    await engine.dispose()
    print("\nSuccess! You can now log in via the frontend with those credentials.")

if __name__ == "__main__":
    asyncio.run(create_admin())
