import asyncio
import asyncpg
import os
from app.config import settings

async def init_db():
    db_url = settings.DATABASE_URL
    pure_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print("Connecting to database...")
    # Render already creates the database, so we just connect directly
    conn = await asyncpg.connect(pure_url)
    
    # Read schema.sql
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    print("Executing schema.sql...")
    try:
        await conn.execute(schema_sql)
        print("Schema initialized successfully.")
    except Exception as e:
        print(f"Error initializing schema: {e}")
        
    await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
