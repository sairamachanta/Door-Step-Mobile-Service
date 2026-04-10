import asyncio
import sys
import os

print("=== init_db.py starting ===", flush=True)

# Add flush to all prints so Render logs show them immediately
def log(msg):
    print(msg, flush=True)

async def init_db():
    try:
        log("Loading config...")
        from app.config import settings
        
        db_url = settings.DATABASE_URL
        pure_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        log(f"Database URL loaded (host: {pure_url.split('@')[1].split('/')[0] if '@' in pure_url else 'unknown'})")
        
        log("Importing asyncpg...")
        import asyncpg
        
        log("Connecting to database...")
        conn = await asyncio.wait_for(
            asyncpg.connect(pure_url),
            timeout=30  # 30 second timeout
        )
        
        # Read schema.sql
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
        
        with open(schema_path, "r") as f:
            schema_sql = f.read()
            
        log("Executing schema.sql...")
        try:
            await conn.execute(schema_sql)
            log("Schema initialized successfully.")
        except Exception as e:
            log(f"Schema warning (may be OK): {e}")
            
        await conn.close()
        log("=== init_db.py complete ===")
        
    except asyncio.TimeoutError:
        log("ERROR: Database connection timed out after 30s")
        sys.exit(1)
    except Exception as e:
        log(f"ERROR in init_db: {type(e).__name__}: {e}")
        # Don't exit with error - let uvicorn still try to start
        # The app's startup event also creates tables via SQLAlchemy

if __name__ == "__main__":
    asyncio.run(init_db())
