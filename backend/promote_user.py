import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import User
from app.config import settings

# This script promotes a user to a specific role for development/testing
# Usage: python promote_user.py <phone> <role>
# Example: python promote_user.py 9988776655 superadmin

async def promote_user(phone, role):
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.phone == phone))
        user = result.scalars().first()
        
        if not user:
            print(f"Error: User with phone {phone} not found.")
            return
        
        user.role = role
        await session.commit()
        print(f"Success: User {user.full_name} ({phone}) has been promoted to {role}.")
    
    await engine.dispose()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python promote_user.py <phone> <role>")
    else:
        phone = sys.argv[1]
        role = sys.argv[2]
        asyncio.run(promote_user(phone, role))
