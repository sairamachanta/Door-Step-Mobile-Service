import asyncio
import asyncpg
import os
from app.config import settings

async def init_db():
    # Parse Database URL to get connection info
    # URL format: postgresql+asyncpg://user:password@host:port/dbname
    # extracting parts manually or using a library would be better, but for now strict parsing
    # assuming standard format from .env
    
    db_url = settings.DATABASE_URL
    # Remove postgresql+asyncpg://
    url_part = db_url.split("://")[1]
    user_pass, host_db = url_part.split("@")
    user, password = user_pass.split(":")
    host_port, dbname = host_db.split("/")
    host, port = host_port.split(":")
    
    print(f"Connecting to postgres on {host}:{port}...")
    
    # Connect to 'postgres' db to check/create target db
    sys_conn = await asyncpg.connect(
        user=user, password=password, host=host, port=port, database='postgres'
    )
    
    # Check if db exists
    exists = await sys_conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    if not exists:
        print(f"Creating database {dbname}...")
        await sys_conn.execute(f"CREATE DATABASE {dbname}")
    else:
        print(f"Database {dbname} already exists.")
        
    await sys_conn.close()
    
    # Connect to target db
    print(f"Connecting to {dbname}...")
    conn = await asyncpg.connect(
        user=user, password=password, host=host, port=port, database=dbname
    )
    
    # Read schema.sql
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "schema.sql")
    # Actually init_db.py is in backend/, so schema.sql is in the same dir
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
