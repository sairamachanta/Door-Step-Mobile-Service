import asyncio
import asyncpg
import os
from app.config import settings

async def update_db():
    db_url = settings.DATABASE_URL
    # Remove postgresql+asyncpg://
    url_part = db_url.split("://")[1]
    user_pass, host_db = url_part.split("@")
    user, password = user_pass.split(":")
    host_port, dbname = host_db.split("/")
    host, port = host_port.split(":")
    
    print(f"Connecting to {dbname} on {host}:{port}...")
    conn = await asyncpg.connect(
        user=user, password=password, host=host, port=port, database=dbname
    )
    
    # Read schema_update.sql
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_update.sql")
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    print("Executing schema_update.sql...")
    try:
        await conn.execute(schema_sql)
        print("Schema updated successfully.")
    except Exception as e:
        print(f"Error updating schema: {e}")
        
    await conn.close()

if __name__ == "__main__":
    asyncio.run(update_db())
