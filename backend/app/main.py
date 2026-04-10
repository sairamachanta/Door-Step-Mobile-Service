from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin

from .routers import auth_router, admin_router, dashboard, bookings, users, subscriptions, technician, metadata
from .config import settings

app = FastAPI(title="Doorstep Services API")

# Automated Table Creation (For initial setup/updates)
@app.on_event("startup")
async def startup_event():
    import os
    import json
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'startup_error.log')
    seeds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seeds')
    
    with open(log_file, 'a') as f:
        f.write(f"\n--- Startup at {datetime.utcnow()} ---\n")
    
    try:
        # Initialize Firebase Admin for verifying Phone Auth tokens
        try:
            if not firebase_admin._apps:
                firebase_admin.initialize_app(options={'projectId': 'mobile-service-7612f'})
        except Exception as fb_err:
            print(f"WARNING: Firebase initialization failed (non-fatal): {fb_err}")
            with open(log_file, 'a') as f:
                f.write(f"Firebase init skipped: {fb_err}\n")
            
        from .database import engine, Base, SessionLocal
        from .models.user import User
        from .utils.security import get_password_hash
        from sqlalchemy import select, func
        import uuid
        
        from . import models 
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            with open(log_file, 'a') as f:
                f.write("Database tables verified/created.\n")

        async with SessionLocal() as session:
            # Seed Banners
            from .models.promotion import Banner
            banner_count = (await session.execute(select(func.count(Banner.id)))).scalar()
            banner_seeds_path = os.path.join(seeds_dir, 'banner_seeds.json')
            if banner_count == 0 and os.path.exists(banner_seeds_path):
                with open(banner_seeds_path, 'r') as f:
                    banner_seeds = json.load(f)
                for b_data in banner_seeds:
                    session.add(Banner(**b_data))
                with open(log_file, 'a') as f:
                    f.write("Seeded initial banners.\n")

            # Seed Protection Plans
            from .models.subscription import ProtectionPlan
            plan_count = (await session.execute(select(func.count(ProtectionPlan.id)))).scalar()
            plan_seeds_path = os.path.join(seeds_dir, 'protection_plan_seeds.json')
            if plan_count == 0 and os.path.exists(plan_seeds_path):
                with open(plan_seeds_path, 'r') as f:
                    plan_seeds = json.load(f)
                for p_data in plan_seeds:
                    session.add(ProtectionPlan(**p_data))
                with open(log_file, 'a') as f:
                    f.write("Seeded initial protection plans.\n")

            # Seed System Metadata
            from .models.system import SystemMetadata
            meta_count = (await session.execute(select(func.count(SystemMetadata.id)))).scalar()
            meta_seeds_path = os.path.join(seeds_dir, 'metadata_seeds.json')
            if meta_count == 0 and os.path.exists(meta_seeds_path):
                with open(meta_seeds_path, 'r') as f:
                    meta_seeds = json.load(f)
                for m_data in meta_seeds:
                    session.add(SystemMetadata(**m_data))
                with open(log_file, 'a') as f:
                    f.write("Seeded initial system metadata.\n")

            # Seed System Settings
            from .models.system import SystemSettings
            settings_count = (await session.execute(select(func.count(SystemSettings.id)))).scalar()
            setting_seeds_path = os.path.join(seeds_dir, 'setting_seeds.json')
            if settings_count == 0 and os.path.exists(setting_seeds_path):
                with open(setting_seeds_path, 'r') as f:
                    setting_seeds = json.load(f)
                for s_data in setting_seeds:
                    session.add(SystemSettings(**s_data))
                with open(log_file, 'a') as f:
                    f.write("Seeded initial system settings.\n")

            await session.commit()
            with open(log_file, 'a') as f:
                f.write("Seeding complete.\n")
                
    except Exception:
        import traceback
        error_trace = traceback.format_exc()
        with open(log_file, 'a') as f:
            f.write(f"STARTUP CRITICAL ERROR:\n{error_trace}\n")
        # Log but don't crash - let uvicorn bind to port
        # DB tables will be created on first successful connection
        print(f"STARTUP WARNING: Database initialization failed. Details logged.\n{error_trace}", flush=True)

# CORS
import os
origins = ["*"]

# Origins are now wildcarded for flexibility
# If specific security is needed later, we can restrict this to FRONTEND_URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Changed to False for wildcard support
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(dashboard.router)
app.include_router(bookings.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(technician.router)
app.include_router(metadata.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Doorstep Services API"}
