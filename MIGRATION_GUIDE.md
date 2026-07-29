# Supabase Migration Guide

This guide covers the necessary steps to transition the AI Learning Management Platform from a local PostgreSQL database to Supabase. This migration retains the existing SQLAlchemy architecture and custom JWT authentication.

## 1. Environment Setup

Update your `backend/.env` file with the Supabase credentials:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-SUPABASE-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[YOUR-SUPABASE-REF].supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

> **Note**: You can find these values in your Supabase project under **Project Settings -> Database** and **Project Settings -> API**.

## 2. Install Dependencies

We have added new dependencies to `requirements.txt`. Install them using:

```bash
cd backend
pip install -r requirements.txt
```

## 3. Database Initialization (Alembic)

We have configured Alembic for database migrations. To sync your existing SQLAlchemy models with your new Supabase database, run the following commands:

```bash
cd backend
alembic revision --autogenerate -m "Initial migration for Supabase"
alembic upgrade head
```

This will automatically create the tables in your Supabase PostgreSQL database based on the existing FastAPI models.

## 4. Supabase Storage and RLS

A SQL script has been provided at `backend/supabase_setup.sql`. 

1. Open the [Supabase SQL Editor](https://app.supabase.com/) for your project.
2. Copy the contents of `backend/supabase_setup.sql`.
3. Run the script. This will:
   - Enable Row Level Security (RLS) on your tables.
   - Set up the `main-bucket` for Supabase Storage.
   - Configure public access policies for uploaded files.

## 5. Storage Service Usage

The `StorageService` in `backend/app/services/storage_service.py` is ready to be used in your API routes for uploading files (e.g., PDFs, profile images).

Example usage:

```python
from app.services.storage_service import storage_service

# To upload a file
public_url = storage_service.upload_file(
    file_bytes=await file.read(), 
    file_name=file.filename,
    content_type=file.content_type
)
```

## 6. Deployment Considerations

When deploying to platforms like Render, Railway, or Fly.io:
1. Ensure all `SUPABASE_*` and `DATABASE_URL` environment variables are securely set.
2. The `database.py` file is already configured to automatically require SSL connections (`sslmode=require`) if connecting to Supabase.
3. Connection pooling is enabled out of the box in SQLAlchemy to handle multiple concurrent requests efficiently.
