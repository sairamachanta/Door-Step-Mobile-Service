# Doorstep Mobile Services Platform

## Overview
This project is a complete authentication system for a mobile repair services platform. It features a FastAPI backend with PostgreSQL and a Vue 3 frontend with Tailwind CSS.

## Tech Stack
- **Backend**: Python FastAPI, SQLAlchemy (Async), PostgreSQL
- **Frontend**: Vue.js 3, Tailwind CSS, Pinia, Vue Router
- **Database**: PostgreSQL

## Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL

## Setup Instructions

### Backend
1. Navigate to the root directory.
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Setup Environment Variables:
   - Check `backend/.env` and update database credentials if needed.
5. Initialize Database:
   ```bash
   python backend/init_db.py
   ```
6. Run Server:
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend
1. Navigate to `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run Development Server:
   ```bash
   npm run dev
   ```
4. Build for Production:
   ```bash
   npm run build
   ```

## Features
- **Authentication**: JWT Access + Refresh Tokens
- **OTP Verification**: Mocked SMS OTP for Signup, Login, and Password Reset
- **Authorization**: Role-based (Customer, Technician, Admin)
- **UI**: Responsive design with Tailwind CSS

## Database Connection
The application connects to a PostgreSQL database using the credentials in `backend/.env`:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/doorstep_services
```

### Steps to Connect:
1. Ensure PostgreSQL is installed and running.
2. Create a database named `doorstep_services`.
3. The application uses `alembic` for migrations or `init_db.py` for initial setup.
   - Run `python backend/init_db.py` to create tables.
4. If you change credentials, update `backend/.env`.

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for the interactive API documentation.
