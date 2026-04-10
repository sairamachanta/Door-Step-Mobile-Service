import asyncio
from app.database import engine
from sqlalchemy import text
from app.config import settings

async def migrate():
    async with engine.begin() as conn:
        print("Altering phone column type to VARCHAR(50)...")
        await conn.execute(text("ALTER TABLE users ALTER COLUMN phone TYPE VARCHAR(50)"))
        
        print(f"Cleaning up possible Root Admin with ID {settings.ROOT_ADMIN_ID}...")
        await conn.execute(text("DELETE FROM users WHERE id = :rid"), {"rid": settings.ROOT_ADMIN_ID})
        print("Done.")

if __name__ == "__main__":
    asyncio.run(migrate())
