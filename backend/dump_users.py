
import asyncio
from app.database import engine
from sqlalchemy import text
import json

async def dump_users():
    try:
        async with engine.connect() as conn:
            res = await conn.execute(text('SELECT id, phone, role, status FROM users'))
            rows = res.fetchall()
            users = [dict(row._mapping) for row in rows]
            with open('users_dump.json', 'w') as f:
                json.dump(users, f, indent=2, default=str)
            print(f"Dumped {len(users)} users")
    except Exception as e:
        with open('error.log', 'w') as f:
            f.write(str(e))

if __name__ == "__main__":
    asyncio.run(dump_users())
