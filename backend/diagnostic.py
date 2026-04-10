
import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())

try:
    from fastapi import FastAPI
    print("FastAPI imported successfully")
except ImportError as e:
    print("FastAPI import FAILED:", e)

try:
    from app.main import app
    print("App imported successfully")
except Exception as e:
    print("App import FAILED:")
    import traceback
    traceback.print_exc()

import asyncio
from app.database import engine
from sqlalchemy import text

async def check_db():
    try:
        async with engine.connect() as conn:
            res = await conn.execute(text('SELECT 1'))
            print("DB connection SUCCESS")
    except Exception as e:
        print("DB connection FAILED:", e)

if __name__ == "__main__":
    asyncio.run(check_db())
