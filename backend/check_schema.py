
import asyncio
from app.database import engine
from sqlalchemy import text
import os

async def check_schema():
    log_path = "/home/sairam_achanta/Documents/Doorstep_mobile_services/backend/schema_audit.log"
    try:
        async with engine.connect() as conn:
            # Check columns of 'users' table
            res = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"))
            columns = [row[0] for row in res.fetchall()]
            with open(log_path, "w") as f:
                f.write(f"Columns in 'users' table: {', '.join(columns)}\n")
                if 'status' not in columns:
                    f.write("CRITICAL: 'status' column is MISSING!\n")
                if 'role' not in columns:
                    f.write("CRITICAL: 'role' column is MISSING!\n")

    except Exception as e:
        with open(log_path, "w") as f:
            f.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(check_schema())
