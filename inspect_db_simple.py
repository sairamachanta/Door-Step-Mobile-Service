import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(os.getcwd())
from backend.app.config import settings

async def inspect_db():
    print(f"Connecting to database...")
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.connect() as conn:
        print("\n--- USERS ---")
        result = await conn.execute(text("SELECT phone, full_name, email, status, is_phone_verified FROM users"))
        users = result.fetchall()
        for user in users:
            print(f"- {user.phone} ({user.full_name}, {user.email}): {user.status}, verified: {user.is_phone_verified}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect_db())
