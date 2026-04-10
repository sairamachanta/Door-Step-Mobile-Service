import asyncio
from app.database import engine
from app.models import User
from sqlalchemy import select
from app.config import settings

async def check():
    print(f"Configured Root Admin Phone: {settings.ROOT_ADMIN_PHONE}")
    print(f"Configured Root Admin ID: {settings.ROOT_ADMIN_ID}")
    
    async with engine.connect() as conn:
        result = await conn.execute(select(User).where(User.phone == settings.ROOT_ADMIN_PHONE))
        user = result.fetchone()
        if user:
            print(f"Found User in DB: {user.full_name}")
            print(f"Actual ID in DB: {user.id}")
            print(f"Match: {user.id == settings.ROOT_ADMIN_ID}")
        else:
            print("Root Admin not found in DB!")

if __name__ == "__main__":
    asyncio.run(check())
